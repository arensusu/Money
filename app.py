
import os
import psycopg2
"""
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode = "require")
cursor = conn.cursor()

cursor.close()
conn.close()
"""
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('/wApXuOouGdvuW1iaOjQ8sSFAV+ahlMJty3AGS5ZTGfZLoPMvVYPn8K2Rx9MaOtEaJ0UnBBKWlZ5UBhXkcgC+q6jRrUb9dfrJvMBlgYkEgYn4XlScGvpH9bTta4xVravDRtOOmui0uB9sYq1EDx02gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('498b5c890e47bbda4135c8a35bf5bd90')

#action list
mainAction = ["新增帳戶", "新增款項", "查閱明細"]
accountAction = ["群組帳戶", "個人帳戶"]
paymentAction = ["收入", "支出"]
listAction = ["本週明細", "本月明細"]

#mention list
mainMention = ["選擇項目(群組帳戶, 個人帳戶)", "選擇項目(收入, 支出)", "選擇項目(本週明細, 本月明細)"]
actionMention = ["請輸入帳戶名稱"]
paymentMention = ["請選擇帳戶", "請輸入品項及金額(ex: 早餐 50)"]

#chat history
main = -1
side = -1

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #choose action
    if main == -1 and side == -1 :
        for i in range(len(mainAction)):
            if event.message.text == mainAction[i]:
                main = i
                """record to chat history"""
                message = TextSendMessage(text = mainMention[i])
                break
            else:
                message = TextSendMessage(text = "error")
        
        line_bot_api.reply_message(event.reply_token, message)


    elif main != -1 and side == -1 :
        action(event, main)
    elif main != -1 and side != -1 :
        action(event, main, side)
    else :
        action()

    """
    if event.message.text == mainAction[0] :
        message = TextSendMessage(text = mainMention[0])
    elif event.message.text == mainAction[1] : 
        message = TextSendMessage(text = mainMention[1])
    elif event.message.text == mainAction[2] :
        message = TextSendMessage(text = mainMention[2])
    else:
        message = TextSendMessage(text="error")
        
    line_bot_api.reply_message(event.reply_token, message)
    """"""
    num = event.source.user_id
    message = TextSendMessage(text=num)
    line_bot_api.reply_message(event.reply_token, message)
    """
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)