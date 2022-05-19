from fastapi import FastAPI, Request, Response
from typing import Optional
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = FastAPI()

line_bot_api = LineBotApi('CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('CHANNEL_SECRET')

@app.get('/hello')
def hello_word():
    return {"hello" : "world"}

@app.post('/message')
async def hello_word(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    
    try:
      handler.handle(body.decode('UTF-8'), signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        if event.message.text == 'สวัสดี' : 
            sendMessage(event,"สวัสดีชาวโลก")
        else:
            echo(event)
    
def echo(event):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
        
def sendMessage(event,message):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))