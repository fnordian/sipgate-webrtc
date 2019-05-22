sipgate webrtc
==============

Small demo to show the capabilities of sipgate's rest-api, oauth2 and webrtc

Getting started
===============

## OAuth2 client setup

Get oauth2 client_id and client_secret from sipgate: https://console.sipgate.com/

For local testing add

 * Redirect URI: http://127.0.0.1:5000/callback
 * Web Origins: http://127.0.0.1:5000

## Run using docker

    sudo docker build -t sipgate-webrtc https://github.com/fnordian/sipgate-webrtc.git
    sudo docker run  -e CLIENT_ID=YOUR_CLIENT_ID -e CLIENT_SECRET=YOUR_CLIENT_SECRET -p 5000:5000 --restart=always -d --name=sipgate-webrtc sipgate-webrtc
