#!/bin/bash
URL=$1
echo $URL
curl -F chat_id="193224174" -F document=@$URL https://api.telegram.org/bot216513681:AAE38YYorq8ox8k1Pnqprn862Ut31SPq3So/sendDocument
