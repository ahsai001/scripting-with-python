#!/usr/bin/env python3

import argparse
import json
import string
import requests
import google.auth.transport.requests

from google.oauth2 import service_account

PROJECT_ID = 'javas-approval'
CREDENTIAL_JSON_FILE = '../../../../Downloads/javas-approval-firebase-adminsdk-u74t5-87d2ec835b.json'


BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

def _get_access_token():
  """Retrieve a valid access token that can be used to authorize requests.

  :return: Access token.
  """
  credentials = service_account.Credentials.from_service_account_file(CREDENTIAL_JSON_FILE, scopes=SCOPES)
  request = google.auth.transport.requests.Request()
  credentials.refresh(request)
  return credentials.token

def _send_fcm_message(fcm_message):
  """Send HTTP request to FCM with given message.

  Args:
    fcm_message: JSON object that will make up the body of the request.
  """
  token = _get_access_token()
  print(token)
  headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json; UTF-8',
  }

  resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)

  if resp.status_code == 200:
    print('Message sent to Firebase for delivery, response:')
    print(resp.text)
  else:
    print('Unable to send message to Firebase')
    print(resp.text)

def _build_common_message(token: string, title: string, body: string, image_url: string = None, data: string = "{}"):
  """Construct common notifiation message.

  Construct a JSON object that will be used to define the
  common parts of a notification message that will be sent
  to any app instance subscribed to the news topic.
  """
  result  = {
    "message":{
        "token":f"{token}",
        "data":{
            "click_action":"FLUTTER_NOTIFICATION_CLICK"
        },
        "notification":{
          "title":f"{title}",
          "body":f"{body}",
          "image":f"{image_url}"
        }
    }
  }
  data_object = json.loads(data)
  result['message']['data'].update(data_object)

  return result

def _build_override_message():
  """Construct common notification message with overrides.

  Constructs a JSON object that will be used to customize
  the messages that are sent to iOS and Android devices.
  """
  fcm_message = _build_common_message()

  apns_override = {
    'payload': {
      'aps': {
        'badge': 1
      }
    },
    'headers': {
      'apns-priority': '10'
    }
  }

  android_override = {
    'notification': {
      'click_action': 'android.intent.action.MAIN'
    }
  }

  fcm_message['message']['android'] = android_override
  fcm_message['message']['apns'] = apns_override

  return fcm_message


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--token')
  parser.add_argument('--title')
  parser.add_argument('--body')
  parser.add_argument('--imageurl')
  parser.add_argument('--data')

  args = parser.parse_args()
  if args.token and args.title and args.body:
    common_message = _build_common_message(args.token, args.title, args.body, args.imageurl, args.data)
    _send_fcm_message(common_message)
  else:
    print('''Invalid command. Please use the following commands:
python sending_fcm.py --token=token --title=title --body=body''')

if __name__ == '__main__':
  main()