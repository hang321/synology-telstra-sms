Using Telstra-SMS for SMS notification on Synology NAS
==============================================

Adapted from https://github.com/miracle2k/synology-sipgate-sms and
https://github.com/marklr/synology-xmpp

DiskStation Manager (DSM) of Synology supports sending SMS notifications by
posting to HTTP url. Recently, Australian telco Telstra is offering a developer
preview for their SMS API, with 1000 SMS message free per month.

This is simple python script to relay the API call between DSM and Telstra SMS API.


Pre-Requisites
--------------

Python and requests module
-------------------
```shell
$ wget https://bootstrap.pypa.io/get-pip.py
$ python get-pip.py
$ pip install requests
```

Installation
------------
```
$ cd /usr/local/
$ curl -k -L https://github.com/hang321/synology-telstra-sms/tarball/master | tar -xzv
$ mv hang321-synology-telstra-sms* telstra-sms
```
Configuration Parameters
-------------------------
in config.py
```
PORT - port number for http server
LOGFILE - location of log file
```

Init script
```
$ mv /usr/local/telstra-sms/S99telstra-sms.sh /usr/syno/etc/rc.d/
```

Start the daemon
```
$ /usr/syno/etc/rc.d/S99telstra-sms.sh start
```

In the administrative UI, configure the SMS provider (Control Panel -> Notification -> SMS -> Add SMS service provider). Name the new provider, e.g. "Telstra SMS API" and use the following url:

    http://localhost:18964/?appkey=&appsecret=&to=&text=hello+world

Press "Next", and assign the following categories:

    appkey = Username
    appsecret = Password
    to = Phone number
    text = Message text

Press "Apply"

    username = your "Consumer Secret" after registered with Telstra API
    password = your "Consumer Key" after registered with Telstra API
    primary number = mobile number

Press the "Send a test SMS message" button to test.


Reference
--------------
https://dev.telstra.com/content/sms-api-0

http://docs.python-requests.org/en/latest/api/

https://github.com/Zachoz/TelstraSMS-PHP
