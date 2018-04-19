# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
from create_reply import MahjongGo
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# state memory
mahjongs = {}

app = Flask(__name__)


# LINE BOT setting
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    global players

    # get msg
    msg = event.message.text

    # get user name
    # group msg
    if event.source.type == "group":
        group_id = event.source.group_id
        user_id = event.source.user_id
        try:
            user_profile = line_bot_api.get_group_member_profile(group_id, user_id)
            user_name = user_profile.display_name
        except LineBotApiError as e:
            # error handle
            print(e)
            user_name = "NoName"
    # user msg
    elif event.source.type == "user":
        user_id = event.source.user_id
        # use user_id insted of groupid
        group_id = user_id
        try:
            user_profile = line_bot_api.get_profile(user_id)
            user_name = user_profile.display_name
        except LineBotApiError as e:
            # error handle
            print(e)
            user_name = "NoName"
    else:
        return
    print("display name", user_name, "group id", group_id, "user id", user_id)

    # if no mahjong object create
    if group_id not in mahjongs:
        mahjongs[group_id] = MahjongGo()

    mahjong = mahjongs[group_id]
    reply = mahjong.createReply(msg, user_name)
    if reply == "":
        return

    if isinstance(reply, list):
        text_msgs = []
        for rep in reply:
            text_msgs.append(TextSendMessage(text=rep))
    else:
        text_msgs = TextSendMessage(text=reply)
    line_bot_api.reply_message(
        event.reply_token,
        text_msgs
    )


if __name__ == "__main__":
    # db.create_all()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
