import requests
import json
from time import sleep
import subprocess
from BeautifulSoup import BeautifulSoup
import urllib2

# This will mark the last update we've checked
with open('updatefile', 'r') as f:
    last_update = int(f.readline().strip())
# Here, insert the token BotFather gave you for your bot.
token = '<token>'
# This is the url for communicating with your bot
url = 'https://api.telegram.org/bot%s/' % token

# We want to keep checking for updates. So this must be a never ending loop
while True:
    # My chat is up and running, I need to maintain it! Get me all chat updates
    get_updates = json.loads(requests.get(url + 'getUpdates', params=dict(offset=last_update)).content)
    # Ok, I've got 'em. Let's iterate through each one
    for update in get_updates['result']:
        # First make sure I haven't read this update yet
        if last_update < update['update_id']:
            last_update = update['update_id']
            f = open( 'updatefile', 'w' )
            f.write(str(last_update))
            f.close()
            # I've got a new update. Let's see what it is.
            if 'message' in update and update['message']['text'][:42] == "https://store.line.me/stickershop/product/":
                # It's a message! Let's send it back :D
                filename = update['message']['text']
                user = update['message']['chat']['id'] 
                stickertitle = BeautifulSoup(urllib2.urlopen(filename)).title.string
                name = update['message']['from']['first_name']
                if 'last_name' in ['message']['from']: name = " ".join((name, update['message']['from']['last_name']))
                requests.get(url + 'sendMessage', params=dict(chat_id=update['message']['chat']['id'], text="Fetching \"" + stickertitle + "\""))
                print name + " (" + str(user) + ")"+ " requested " + filename
                subprocess.call("./imagedl.sh " + filename + " " + str(user), shell=True)
            else:
                 requests.get(url + 'sendMessage', params=dict(chat_id=update['message']['chat']['id'], text="That doesn't appear to be a valid URL. To start, send me a URL that starts with \"https://store.line.me/stickershop/product/\""))
    # Let's wait a few seconds for new updates
    sleep(3)
