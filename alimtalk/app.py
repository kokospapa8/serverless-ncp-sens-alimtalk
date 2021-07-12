import os
import hashlib
import hmac
import base64
import requests
import time

SERVICE_ID = os.environ["SERVICE_ID"]
NAVER_ACCESS_KEY = os.environ['NAVER_ACCESS_KEY']
NAVER_SECRET_KEY = os.environ['NAVER_SECRET_KEY']
PLUS_FIREND_ID = os.environ['PLUS_FIREND_ID']


def lambda_handler(event, context):
    # print("Received payload: " + json.dumps(event))
    messages = event["messages"]
    template_code = event["template_code"]

    uri = f"/alimtalk/v2/services/{SERVICE_ID}/messages"
    url = f"https://sens.apigw.ntruss.com{uri}"

    payload = {
        "plusFriendId": PLUS_FIREND_ID,
        "templateCode": template_code,
        "messages": messages
    }

    timestamp = str(int(time.time() * 1000))
    signature = make_signature(uri, timestamp)

    headers = {"Content-Type": "application/json",
               "x-ncp-apigw-timestamp": timestamp,
               "x-ncp-iam-access-key": NAVER_ACCESS_KEY,
               "x-ncp-apigw-signature-v2": signature
               }

    r = requests.post(url, json=payload, headers=headers)
    return {"status": r.status_code}


def make_signature(uri, timestamp):

    access_key = NAVER_ACCESS_KEY				# access key id (from portal or Sub Account)
    secret_key = NAVER_SECRET_KEY				# secret key (from portal or Sub Account)
    secret_key = bytes(secret_key, 'UTF-8')

    method = "POST"
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signing_key = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signing_key
