from getpass import getpass
from beablooAPI import (get_key,
                        get_message_list,
                        create_message,
                        remove_message,
                        edit_message,
                        base64_encode)
from body import beabloo_body

# define a class to store credentials
class Credential:
    pass


key = ''
authenticated = False
while not authenticated:
    # prompt user for credentials
    user = Credential()
    user.username = input("Enter your Beabloo CMS username: ")
    user.password = getpass(prompt="Password (hidden): ",
                            stream=None)

    # try login
    key = get_key(user.username, user.password)
    if not key:
        continue
    authenticated = True
    key = key[1]

# See what actions the user wants to preform
option = False
while not option:
    print('Please select an action to preform:'
          + '\n 1. Upload new test messages with dummy data'
          + '\n 2. Remove all messages in channel'
          + '\n 3. Edit all messages in channel with dummy data'
          + '\n 4. Exit')
    option_selected = input('Choice: ')
    try:
        val = int(option_selected)
        if val not in range(1, 3):
            print("Please select from the given options \n e.g. 1")

        # Option 1 | Upload to new messages
        if val == 1:
            # complete dummy body and upload
            beabloo_body["title"] = "Upload Test"
            beabloo_body["attachment"]["fileContent"] = base64_encode('assets/main.jpg')
            beabloo_body['additionalFields'].append({
                "key": "testField",
                "type": "TEXT",
                "value": "this is a upload test"
            })

            count = 0
            while count < 5:
                new_message = create_message(key, '56787', beabloo_body)
                if not new_message:
                    print('Issue uploading message')
                else:
                    print('New message id: '
                          + str(new_message[1]))
                count += 1

        if val == 2:
            old_message_list = get_message_list(key, '56787')
            if not old_message_list:
                print('Could not get data from channel')
            else:
                old_message_list = old_message_list[1]
                for i in old_message_list:
                    remove_message(key, i)

        if val == 3:
            # complete dummy body and upload
            beabloo_body["title"] = "Edit Test"
            beabloo_body["attachment"]["fileContent"] = base64_encode('assets/edit.jpg')

            old_message_list = get_message_list(key, '56787')
            if not old_message_list:
                print('Could not get data from channel')

            else:
                old_message_list = old_message_list[1]
                for message in old_message_list:
                    edited_message = edit_message(key, message, beabloo_body)
                    if not edited_message:
                        print('Issue editing message')
                    else:
                        print('Edited message: '
                              + str(message))

        if val == 4:
            option = True

    except ValueError:
        print("Value Error: Please enter an integer")

