"""
This file contains some functions for
auth, upload and removal of messages from
Beabloo CMS

Additionally this file contains some necessary
function for processing the upload body for
new messages
(base64_encode, remove_emoji)
"""
import requests, json, base64, sys
from logger import log

base_url = "https://cms.beabloo.com/engine2/rest/cms/api/v2/"


def get_key(username, password):
    s = requests.Session()  # init requests

    # set up request
    headers = {'Content-Type': 'application/json'}
    body = {"username": username, "password": password}

    request = s.post(base_url + 'auth/',
                     data=json.dumps(body),
                     headers=headers,
                     timeout=10)
    if request.status_code != 200:
        print('Error logging in status code: '
              + str(request.status_code))
        return False
    else:
        print('Login Successful')
        return True, request.text


def create_message(key, channel_id, body, logging=None):
    s = requests.Session()
    headers = {"Authorization": key, 'Content-Type': 'application/json'}
    request = s.post(base_url + 'channels/' + channel_id + "/posts/",
                     data=json.dumps(body),
                     headers=headers,
                     timeout=10)
    if request.status_code != 200:
        print('Error uploading message status code: '
              + str(request.status_code))
        print(request.text)
        log(headers, body)
        return False
    else:
        data = json.loads(request.text)
        if logging:
            log(headers, body, data["id"])
        return True, data["id"]


def edit_message(key, message_id, body, logging=None):
    s = requests.Session()
    headers = {"Authorization": key, 'Content-Type': 'application/json'}
    request = s.put(base_url + 'posts/' + str(message_id),
                    data=json.dumps(body),
                    headers=headers)
    if request.status_code != 200:
        print('Error editing message status code: '
              + str(request.status_code))
        return False
    else:
        data = json.loads(request.text)
        if logging:
            log(headers, body, data["id"])
        return True


def get_message_list(key, channel_id):
    s = requests.Session()
    headers = {"Authorization": key}
    request = s.get(base_url + 'channels/' + channel_id + "/posts/",
                    headers=headers)
    if request.status_code != 200:
        return False
    else:
        message_list = []
        message_data = json.loads(request.text)
        for i in message_data:
            message_list.append(i["id"])
        return True, message_list


def remove_message(key, message_id):
    s = requests.Session()
    headers = {"Authorization": key, 'Content-Type': 'application/json'}
    request = s.delete(base_url + "posts/" + str(message_id),
                       headers=headers)
    if request.status_code == 204:
        data = request.text
        print("removed message : " + str(message_id))
        return data
    else:
        print("error")
        print(request.status_code)


# --- Extras for beabloo --- #

def base64_encode(file):
    with open(file, 'rb') as f:
        data = f.read()
        b64string = base64.b64encode(data).decode("utf-8")
        return b64string
