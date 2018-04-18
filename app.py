# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import random
import create_reply
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    StickerMessage, StickerSendMessage,
)

# state
players = []

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
    group_id = event.source.group_id,
    user_id = event.source.user_id,
#    user_profile = line_bot_api.get_profile(user_id)
    user_profile = line_bot_api.get_group_member_profile(group_id, user_id)
    user_name = user_profile.display_name
    msg = event.message.text

    reply, num_player = create_reply.createReply(msg, user_name, players)
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


@handler.add(MessageEvent, message=StickerMessage)
def message_sticker(event):
    sticker_id = random.randint(180, 307)
    if sticker_id < 260:
        package_id = 3
    else:
        package_id = 4

    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=package_id,
            sticker_id=sticker_id,
        )
    )




if __name__ == "__main__":
    # db.create_all()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
