#!/bin/bash
URL=$1
CHAT=$2
cd downloads
wget -q -x -p --convert-links $URL
FIRST=${URL#"https://"}
SECOND=${FIRST/stickershop\/product\/*\/en/''}
cd $SECOND
grep 'width: [0-9]*px; height: [0-9]*px; background-image:url(' ./stickershop/product/*/en > stickerlines
sed 's/                          <span class=".*" style="width: [0-9]*px; height: [0-9]*px; background-image:url(//g' stickerlines >> newstickers
sed 's/); background-size: [0-9]*px [0-9]*px;" data-sticker-id=".*"><\/span>//g' newstickers >> neweststickers
rm stickerlines
rm newstickers
wget -i neweststickers -P stickerfolder
cd stickerfolder
convert *.png -filter sinc -resize 512x512 sticker.png
zip stickers.zip ./sticker-*.png
curl -F chat_id=$CHAT -F document=@"stickers.zip" https://api.telegram.org/bot216513681:AAE38YYorq8ox8k1Pnqprn862Ut31SPq3So/sendDocument
cd ../..
rm -rf store.line.me
