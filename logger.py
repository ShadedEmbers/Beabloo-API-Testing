import json


# Log request data in json format
# TODO Find better way to log data
def log(headers=None, body=None, message_id=None):
    with open('logs/request_' + str(message_id) + '.json', 'w') as file:
        request_content = {
            "request": {
                "body": body,
                "headers": headers
            }
        }
        file.write(json.dumps(request_content, indent=4, sort_keys=True))
        file.close()
