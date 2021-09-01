
from datetime import date

import os
import psycopg2

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
#mainAction = ["新增帳戶", "新增款項", "查閱明細"]
mainAction = ["新增帳戶", "查閱明細"]
accountAction = ["群組帳戶", "個人帳戶"]
#paymentAction = ["收入", "支出"]
listAction = ["本週明細", "本月明細"]

#mention list
#mainMention = ["選擇項目(群組帳戶, 個人帳戶)", "選擇項目(收入, 支出)", "選擇項目(本週明細, 本月明細)"]
mainMention = ["選擇項目(群組帳戶, 個人帳戶)", "選擇項目(本週明細, 本月明細)"]
actionMention = ["請輸入帳戶名稱"]
#paymentMention = ["請選擇帳戶", "請輸入品項及金額(ex: 早餐 50)"]

#datebase

def dbConnect():
    database = "de2autom7hvb"
    user = "cdwdunsupuvvkj"
    pw = "94ff64c4bd76e17fe85202095d37123faa46ab382706801cdcac9c83938b6e4a"
    host = "ec2-44-194-183-115.compute-1.amazonaws.com"
    port = "5432"

    conn = psycopg2.connect(database = database, user = user, password = pw, host = host, port = port)
    cursor = conn.cursor()

    return (conn, cursor)

def checkHistory():

    conn, cursor = dbConnect()

    sql = '''SELECT chat FROM chat;'''

    cursor.execute(sql)
    chatList = cursor.fetchall()

    if len(chatList) > 0:
        main = chatList[0]

    if len(chatList) > 1:
        side = chatList[1]

def recordChat(message):
    
    conn, cursor = dbConnect()

    sql = '''INSERT INTO chat(chat) VALUES(%s);'''
    
    cursor.execute(sql, (message, ))
    conn.commit()

    cursor.close()
    conn.close()

def clearChat():
    
    conn, cursor = dbConnect()

    sql = '''DELETE FROM chat;'''
    
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

def recordPayment(messageList, timestamp):

    conn, cursor = dbConnect()

    insertSQL = '''INSERT INTO outcome(account, month, day, amount, remark) VALUES(%s, %s, %s, %s, %s);'''
    print(date.fromtimestamp(timestamp))
    cursor.execute(insertSQL, (messageList[0], date.fromtimestamp(timestamp).month, date.fromtimestamp(timestamp).day, messageList[2], messageList[1], ))

    fetchSQL = '''SELECT amount FROM balance WHERE account = %s;'''
    cursor.execute(fetchSQL, (messageList[0], ))

    money, = cursor.fetchone()
    money += int(messageList[2])

    updateSQL = '''UPDATE balance SET amount = %s WHERE account = %s;'''
    cursor.execute(updateSQL, (money, messageList[0], ))

    conn.commit()

    cursor.close()
    conn.close()

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
    #chat history
    main = -1
    side = -1
    
    #choose action
    if main == -1 and side == -1 :
        messageList = event.message.text.split(' ')
        timestamp = event.timestamp / 1000
        print(timestamp)

        if len(messageList) == 3:
            recordPayment(messageList, timestamp)
            message = TextSendMessage(text = '已存入')
            line_bot_api.reply_message(event.reply_token, message)

        """for i in range(len(mainAction)):
            if event.message.text == mainAction[i]:
                recordChat(i)
                message = TextSendMessage(text = mainMention[i])
                break
            else:
                clearChat()
                message = TextSendMessage(text = "error")
        
        line_bot_api.reply_message(event.reply_token, message)
    """
    elif main != -1 and side == -1 :
        """check action match"""
        """record to chat history"""
        message = TextSendMessage(text = mainMention[main])
        line_bot_api.reply_message(event.reply_token, message)

    elif main != -1 and side != -1 :
        #action(event, main, side)
        if main == 0:
            message = TextSendMessage(text = "account")
        elif main == 1:
            message = TextSendMessage(text = "payment")
        elif main == 2:
            message = TextSendMessage(text = "list")
        else:
            message = TextSendMessage(text = "detailError")
        
        line_bot_api.reply_message(event.reply_token, message)

    else :
        #action()
        message = TextSendMessage(text = "mainError")
        line_bot_api.reply_message(event.reply_token, message)

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