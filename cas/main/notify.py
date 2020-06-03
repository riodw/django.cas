# notify.py
import argparse
import requests
import datetime
import pytz
import time

BASE_URL = 'https://notify.zappa_notify.com/api/'
EMAIL_URL = 'email/'
SMS_URL = 'sms/'

tz = pytz.timezone('US/Eastern')

data_preset = {
    'source': 'account.this_url.com',
    'subject': 'Sigup ccount email',
    'recipient': 'riodweber@gmail.com',
    'message': 'Email from django.cas\nTime: ' + str(datetime.datetime.now(tz=tz)),
    'datetime': str(datetime.datetime.now(tz=tz))
}
# 'datetime': datetime.datetime.now(tz=tz) + datetime.timedelta(minutes=1)
# 2017-10-26 16:26:37.644379-04:00


def send_email(subject, recipient, message, datetime=''):
    print('Sending Email')
    data = data_preset
    data['subject'] = subject
    data['recipient'] = recipient
    data['message'] = message
    if datetime:
        data['datetime'] = datetime

    try:
        r = requests.post(BASE_URL + EMAIL_URL, data=data)
        response = r.json()
        if 'public_id' in response:
            print('Your notification public_id is:', response['public_id'])
            return response['public_id']
        else:
            print('ERROR: No "public_id" from notify server.')
            print(response)
    except:
        print('Failed to send request')
        return 0