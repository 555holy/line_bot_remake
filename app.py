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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()