from flask import Flask, request, abort
from linebot import WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
from collections import namedtuple
from datetime import datetime
from utils import send_message
#------FSM------#
from fsm import TocMachine
from states import chatbot_states_config

app = Flask(__name__)

# for line
CHANNEL_SECRET = os.environ.get('Line_ChatBot_Secret')
parser = WebhookParser(CHANNEL_SECRET)

user_machine = {}

#===================================================
#   futures bot
#===================================================
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then reply
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        # create FMS machine for user
        user_id = str(event.source.user_id)
        if(user_id not in user_machine.keys()):
            user_machine[user_id] = TocMachine(id=user_id, **chatbot_states_config)
        machine = user_machine[user_id]        
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        # if response == False:
        #     content = '輸入錯誤！\n請參考：\n1.輸入"me or Me", 回傳自己的id\n2.輸入data20190130, 日期格式為4位數年2位數月2位數日期,得到那日的開高低收\n3.輸入fig20190130, 日期格式同上, 得到那天的分k圖表資料'

    return 'OK'

@app.route("/", methods=['GET'])
def basic_url():
    return 'OK'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9900, debug=True, 
            ssl_context=('./ssl/certificate.pem', './ssl/private.key'))