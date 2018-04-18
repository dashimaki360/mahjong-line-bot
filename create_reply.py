# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import random

RESPONSE_DICT = {
        '麻雀1': 'ひとりでは麻雀はできんぞ',
        'まーじゃん1': 'ひとりでは麻雀はできんぞ',
        'マージャン1': 'ひとりでは麻雀はできんぞ'
        }
FIX_REPLY_LIST = [
    "麻雀がしたくなったら\"麻雀1\"と言ってくれ"
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
        if dictKey.lower() in msg.lower():
            value = RESPONSE_DICT[dictKey]
            # check value is list or nor and rand choice
            reply = detectMsg(value)
            return reply

    reply = random.choice(FIX_REPLY_LIST)
    return reply


def createReply(txt_msg):
    reply = dictMsg(txt_msg)
    return reply
