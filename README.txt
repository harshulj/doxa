Doxa
===================
Doxa is a Polling and Opinion ranking system.

Harshul Jain


Some Commands
================
Heroku setting for sending mail:

import os
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST= 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']


Run development mail server
python -m smtpd -n -c DebuggingServer localhost:1025
