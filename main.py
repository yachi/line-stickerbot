import json
import logging
from time import sleep
import urllib.request
import urllib.parse
import requests
import cssutils
from bs4 import BeautifulSoup
from wand.image import Image
from zipfile import ZipFile
from OpenSSL import SSL
import os
import hashlib

cssutils.log.setLevel(logging.CRITICAL)


# This will mark the last update we've checked
with open('updatefile', 'r') as f:
    last_update = int(f.readline().strip())
# Here, insert the token BotFather gave you for your bot.
TOKEN = os.environ['TOKEN']
# This is the url for communicating with your bot
URL = 'https://api.telegram.org/bot%s/' % TOKEN

# The Line store URL format.
LINE_URL = "https://store.line.me/stickershop/product/"

# The text to display when the sent URL doesn't match.
WRONG_URL_TEXT = ("That doesn't appear to be a valid URL. "
                  "To start, send me a URL that starts with " + LINE_URL)

def dl_stickers(page):
    images = page.find_all('span', attrs={"style": not ""})
    for i in images:
        imageurl = i['style']
        imageurl = cssutils.parseStyle(imageurl)
        imageurl = imageurl['background-image']
        imageurl = imageurl.replace('url(', '').replace(')', '')
        imageurl = imageurl[1:-15]
        print(imageurl)
        response = urllib.request.urlopen(imageurl)
        resize_sticker(response, imageurl)

def resize_sticker(image, filename):
    filet = filename[-4:]
    filen = hashlib.sha224(filename.encode('utf-8')).hexdigest() + filet
    print(filen)
    with Image(file=image) as img:
        ratio = 1
        if img.width > img.height:
            ratio = 512.0/img.width
        else:
            ratio = 512.0/img.height
        img.resize(int(img.width*ratio), int(img.height*ratio), 'mitchell')
        img.save(filename=("downloads/" + filen))

def send_stickers(page):
    dl_stickers(page)
    with ZipFile('stickers.zip', 'w') as stickerzip:
        for root, dirs, files in os.walk("downloads/"):
            for file in files:
                stickerzip.write(os.path.join(root, file))
                os.remove(os.path.join(root, file))
    requests.post(URL + 'sendDocument', params=dict(
        chat_id = update['message']['chat']['id']
    ), files=dict(
        document = open('stickers.zip', 'rb')
    ))
    print("snet;)")


# We want to keep checking for updates. So this must be a never ending loop
while True:
    # My chat is up and running, I need to maintain it! Get me all chat updates
    get_updates = json.loads(requests.get(URL + 'getUpdates',
                                          params=dict(offset=last_update)).content.decode())
    # Ok, I've got 'em. Let's iterate through each one
    for update in get_updates['result']:
        # First make sure I haven't read this update yet
        if last_update < update['update_id']:
            last_update = update['update_id']
            f = open('updatefile', 'w')
            f.write(str(last_update))
            f.close()
            # I've got a new update. Let's see what it is.
            if 'message' in update:
                if update['message']['text'][:42] == LINE_URL:
                    # It's a message! Let's send it back :D
                    sticker_url = update['message']['text']
                    user = update['message']['chat']['id']
                    request = requests.get(sticker_url).text
                    stickerpage = BeautifulSoup(request, "html.parser")
                    stickertitle = stickerpage.title.string
                    name = update['message']['from']['first_name']
                    requests.get(URL + 'sendMessage',
                                 params=dict(chat_id=update['message']['chat']['id'],
                                             text="Fetching \"" + stickertitle + "\""))
                    print(name + " (" + str(user) + ")"+ " requested " + sticker_url)
                    send_stickers(stickerpage)
                else:
                    requests.get(URL + 'sendMessage',
                                 params=dict(chat_id=update['message']['chat']['id'],
                                             text=WRONG_URL_TEXT))
    # Let's wait a few seconds for new updates
    sleep(1)


