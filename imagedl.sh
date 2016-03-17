#!/bin/bash
URL=$1
CHAT=$2
cd downloads
wget -q -x -p --convert-links $URL
FIRST=${URL#"https://"}
SECOND=${FIRST/stickershop\/product\/*\/*/''}
cd $SECOND
grep 'width: [0-9]*px; height: [0-9]*px; background-image:url(' ./stickershop/product/*/* > stickerlines
sed 's/                          <span class=".*" style="width: [0-9]*px; height: [0-9]*px; background-image:url(//g' stickerlines >> newstickers
sed 's/); background-size: [0-9]*px [0-9]*px;" data-sticker-id=".*"><\/span>//g' newstickers >> neweststickers
rm stickerlines
rm newstickers
wget -q -i neweststickers -P stickerfolder
cd stickerfolder
convert *.png -filter sinc -resize 512x512 sticker.png
zip -q stickers.zip ./sticker-*.png
curl -s -F chat_id=$CHAT -F document=@"stickers.zip" https://api.telegram.org/bot<token>/sendDocument > /dev/null
cd ..
rm -rf stickerfolder
rm neweststickers
cd ..
rm -rf store.line.me
cd ..
