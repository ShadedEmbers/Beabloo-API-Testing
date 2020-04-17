from time import time

publication_date = str(int(time())) + str("000")
expire_date = str(int(time() + 31536000)) + str("000")

beabloo_body = {
    "publicationDate": publication_date,
    "expirationDate": expire_date,
    "attachment": {
        "name": str(publication_date + ".jpg"),
        "operation": "REPLACE"
    },
    "additionalFields": []
}

