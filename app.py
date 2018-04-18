# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import random
from datetime import datetime

import create_reply

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy

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

# heroku postgresql setting
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class usermessage(db.Model):
    '''
    user message and reply db
    '''
    __tablename__ = 'usermessage'
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50))
    message = db.Column(db.Text)
    reply_message = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP)

    def __init__(self,
                 id,
                 user_id,
                 message,
                 reply_message,
                 timestamp,):
        self.id = id
        self.user_id = user_id
        self.message = message
        self.reply_message = reply_message
        self.timestamp = timestamp

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            message=self.message,
            reply_message=self.reply_message,
            timestamp=self.timestamp,
        )


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


def addToSql(event, reply, sticker=False, image=False):
    '''
    add message data to sql
    '''
    if sticker:
        msg = "stamp {} {}".format(event.message.package_id, event.message.sticker_id)
    elif image:
        msg = "IMAGE_MESSAGE"
    else:
        msg = event.message.text,
    add_data = usermessage(
            id=event.message.id,
            user_id=event.source.user_id,
            message=msg,
            reply_message=reply,
            timestamp=datetime.fromtimestamp(int(event.timestamp)/1000)
        )
    try:
        db.session.add(add_data)
        db.session.commit()
    except (SQLAlchemy.exc.SQLAlchemyError, SQLAlchemy.exc.DBAPIError) as e:
        print("sql error happen")
        print(e)


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    msg = event.message.text
    reply = create_reply.createReply(msg)

    if isinstance(reply, list):
        text_msgs = []
        for rep in reply:
            text_msgs.append(TextSendMessage(text=rep))
        rec_msg = ','.join(reply)
    else:
        text_msgs = TextSendMessage(text=reply)
        rec_msg = reply

    line_bot_api.reply_message(
        event.reply_token,
        text_msgs
    )
#    addToSql(event, rec_msg)


@handler.add(MessageEvent, message=StickerMessage)
def message_sticker(event):
    sticker_id = random.randint(180, 307)
    if sticker_id < 260:
        package_id = 3
    else:
        package_id = 4
    reply = "stamp {} {}".format(package_id, sticker_id)

#    addToSql(event, reply, sticker=True)

    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=package_id,
            sticker_id=sticker_id,
        )
    )


if __name__ == "__main__":
    db.create_all()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
