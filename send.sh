#!/bin/bash

TOKEN=$3
CHAT_ID=$1
MESSAGE=$2
URL="https://api.telegram.org/bot$TOKEN/sendMessage"

curl -s -X POST $URL -d chat_id=$CHAT_ID -d text="$MESSAGE" 
