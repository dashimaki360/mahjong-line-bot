# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random


class MahjongGo():
    def __init__(self):
        self.RESPONSE_DICT = {
                '麻雀1': '1!',
                'まーじゃん1': '1!',
                'マージャン1': '1!'
                }
        self.players = []

    def createReply(self, txt_msg, user_name):
        reply = ""
        num_player = len(self.players)

        if num_player > 0 and txt_msg == "解散":
                reply = "解散!"
                self.players = []
                return reply

        if num_player == 0:
            if txt_msg in self.RESPONSE_DICT:
                reply = "1! " + user_name
                self.players.append(user_name)
        elif num_player == 1:
            if txt_msg == "2":
                reply = "2! " + user_name
                self.players.append(user_name)
        elif num_player == 2:
            if txt_msg == "3":
                reply = "3! " + user_name
                self.players.append(user_name)
        elif num_player == 3:
            if txt_msg == "4":
                self.players.append(user_name)
                rnd_players = random.sample(self.players, len(self.players))
                reply = ["4! " + user_name,
                         "GO!\n" +
                         "東: " + rnd_players[0] + "\n" +
                         "南: " + rnd_players[1] + "\n" +
                         "西: " + rnd_players[2] + "\n" +
                         "北: " + rnd_players[3]
                         ]
                self.players = []
        else:
            reply = "I have a bag players {}".format(self.players)

        return reply
