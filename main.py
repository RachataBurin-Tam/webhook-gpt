import json
from flask import Flask, request, abort, jsonify
from azure_openai import ask_azure_gpt

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
app = Flask(__name__)


line_bot_api = LineBotApi("h/xd2pSMcnQDc0Uw6f+BCW0Cpc0BFe/3HWi5IhMi/qN5YF8SpmKntct0dTmt7kgGjahIntJg2PxhNBcZDq/C1mGPF/nMM9hQt/P4ogl2+GEkJg7CNYYF+Q2eafh4E51JU9p5dZpeQQ7fo7Lv6DLfAwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("24f1138e3838867bceeef2e84f1fecaa")

# Route / with GET method return Welcome message
@app.route("/", methods=['GET'])
def index():
    return "Welcome to MBK Line Bot"

# Route /message with GET method and q parameter
@app.route("/message", methods=['GET'])
def message():
    # Get query parameter
    query = request.args.get('q')
    answer = ask_azure_gpt(query)

    # return answer as json​
    return jsonify({"question": query, "answer": answer})

@app.route("/direct", methods=['POST'])
def direct():
    body = request.get_data(as_text=True)
    answer = ask_azure_gpt(body)
    return json.loads(answer)


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
    answer = ask_azure_gpt(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=answer))


if __name__ == "__main__":
    
    print("Starting Flask OpenAI app")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)


