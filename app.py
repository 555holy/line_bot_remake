from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('ByvjX61CbFyjmFH8bZEcQkMmgYxdbM4LPi/eKqBsTh/Gx/ToTjGGaUVi09WtgBh8Gs+MUKev4PDHKrHge9egZh2GAh/ozxfp82/0JZ0+nN9xO4bMgebO16UAG99EbSP+oZg9D3Kf0C9VX+TStRou+wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('72d159a2a425fd40d73407d6a13ff37d')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '我聽不懂，說人話可以嗎?'
    
    if msg in ['hi', 'Hi']:
        r = 'hi，在幹嘛?'
    elif msg == '我要PS5':
        r = '我也想要，下次一起搶'
    elif msg =='我想定位':
        r = '好喔'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()