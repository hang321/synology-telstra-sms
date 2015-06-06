#!/usr/bin/env python
"""
https://github.com/hang321/synology-telstra-sms
"""

import requests, json


class TelstraSmsApi(object):
    def __init__(self, appkey, appsecret):
        self.appkey = appkey
        self.appsecret = appsecret


    def authenticate(self):
        "To get an OAuth 2.0 authentication token"

        url = "https://api.telstra.com/v1/oauth/token"
        payload = {
            'client_id': self.appkey,
            'client_secret': self.appsecret,
            'grant_type': 'client_credentials',
            'scope': 'SMS'
        }
        response = requests.get(url, params=payload)

        accessToken = response.json()['access_token']
        #print accessToken
        return accessToken


    def sendMessage(self, token, recipient, message ):
        "use the token from authentication to send SMS message"

        url = "https://api.telstra.com/v1/sms/messages"
        headers = {
            'Content-Type': 'application/json',
            'Authorization ': 'Bearer ' + str(token)
        }
        # print headers

        payload = {
            'to': recipient,
            'body': message
        }
        data = json.dumps(payload)
        # print data

        response = requests.post(url, data=data, headers=headers)
        #print response.text
        return response.text
