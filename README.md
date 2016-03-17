# line-stickerbot
A Telegram bot for downloading Line stickers. It takes a URL sent to the bot from a user, downloads the page, and finds the relevant image links. Then, it downloads the images, rescales them to the appropriate size, and sends them all back to the user in a .zip archive.

## How do I use it?
Add [@line_stickerbot](http://telegram.me/line_stickerbot) on Telegram.

Or, if you prefer to run it yourself, replace `<token>` in `main.py` and `imagedl.sh` with the token the Botfather gave you, and run `main.py`.

## Dependencies

The script should work fine on any Unix-like out of the box, but just in case:

### Software
* *wget* For fetching the webpage and images.
* *grep* For finding the image links in the webpage.
* *sed* For finding the image links in the webpage.
* *imagemagick* For resizing the images to the correct size.
* *curl* For posting the file to send to the user.

### Python Modules
* *urllib2* For fetching the webpage.
* *BeautifulSoup* For parsing the HTML and fetching the page Title.

## Wait, what? You're fetching the page multiple times? And why is half of this a shell script while the other half is in Python?
I'm aware it's terrible. I'm very new to all this, and most of it is copy-pasted from Google. Hopefully I'll do a proper rewrite soon enough. Feel free to submit a pull request if you want to fix it.
