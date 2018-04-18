# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import random

RESPONSE_DICT = {
        '麻雀1': '1!',
        'まーじゃん1': '1!',
        'マージャン1': '1!'
        }
FIX_REPLY_LIST = [
    ""
]


def detectMsg(msgs):
    if isinstance(msgs, list):
        det_msgs = []
        for msg in msgs:
            if isinstance(msg, list):
                msg = random.choice(msg)
            det_msgs.append(msg)
        reply = det_msgs
    else:
        reply = msgs
    return reply


def dictMsg(msg):
    for dictKey in RESPONSE_DICT.keys():
        if dictKey.lower() == msg.lower():
            value = RESPONSE_DICT[dictKey]
            # check value is list or nor and rand choice
            reply = detectMsg(value)
            return reply

    reply = random.choice(FIX_REPLY_LIST)
    return reply


def createReply(txt_msg, num_player):
    reply = ""
    if num_player == 0:
        if txt_msg in RESPONSE_DICT:
            reply = "1!"
            num_player = 1
    elif num_player == 1:
        if txt_msg == "2":
            reply = "2!"
            num_player = 2
    elif num_player == 2:
        if txt_msg == "3":
            reply = "3!"
            num_player = 3
    elif num_player == 3:
        if txt_msg == "4":
            reply = ["4!", "GO!"]
            num_player = 0
    else:
        reply = "I have a bag player num is {}".format(num_player)

    return reply, num_player
