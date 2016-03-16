#!/bin/bash
URL=$1
cd downloads
wget -q -x $URL
cd ${URL#"http://"}
zip -r website.zip ./*
curl -F chat_id="193224174" -F document=@"website.zip" https://api.telegram.org/bot216513681:AAE38YYorq8ox8k1Pnqprn862Ut31SPq3So/sendDocument
