from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import datetime
import json
import boto3
import requests

from database import *

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

richID = "richmenu-4ccab11c32e10ca40b6716945b5096aa"
headers = {"Authorization":"Bearer /wApXuOouGdvuW1iaOjQ8sSFAV+ahlMJty3AGS5ZTGfZLoPMvVYPn8K2Rx9MaOtEaJ0UnBBKWlZ5UBhXkcgC+q6jRrUb9dfrJvMBlgYkEgYn4XlScGvpH9bTta4xVravDRtOOmui0uB9sYq1EDx02gdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+richID, headers=headers)

money = Accounting()

#action list
summaryAction = ["週結算", "月結算", "年結算"]

def RecordPayment(messageList):
    date = datetime.datetime.now()
    return money.AddOutcome(messageList[0], date, messageList[1], int(messageList[2]))

def PrintPayment(messageList):
    user = messageList[0]
    type = messageList[1]
    period = messageList[2].zfill(2)

    return money.PrintSummary(user, type, period)

def lambda_handler(event, context):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        #choose action
        messageList = event.message.text.split(' ')

        for action in summaryAction:
            money.Summary(messageList[0], action)

        if messageList[1] in summaryAction:
            message = TextSendMessage(text = PrintPayment(messageList))
            line_bot_api.reply_message(event.reply_token, message)

        else:
            message = TextSendMessage(text = RecordPayment(messageList))
            line_bot_api.reply_message(event.reply_token, message)

            
    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']

    # get request body as text
    body = event['body']

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            'statusCode': 502,
            'body': json.dumps("Invalid signature. Please check your channel access token/channel secret.")
            }
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from Lambda!")
        }