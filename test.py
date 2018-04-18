# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import create_reply as cre


class TestShirotan(unittest.TestCase):
    """test class of create_reply.py
    """

    def test_dict1(self):
        EXPECTED_REPLY = 'ひとりでは麻雀はできんぞ'
        test_msgs = [
          "麻雀1",
          "まーじゃん1",
          "マージャン1",
        ]
        for msg in test_msgs:
            self.assertEqual(EXPECTED_REPLY, cre.dictMsg(msg))

    def test_dict_fix(self):
        EXPECTED_REPLY_LIST = [
           "麻雀がしたくなったら\"麻雀1\"と言ってくれ"
        ]
        test_msgs = [
          "しね",
          "おまえなんてきらいだ",
          "東京ビックサイトはどっちですか?",
          "またねー",
          "しね",
          "おまえなんてきらいだ",
          "東京ビックサイトはどっちですか?",
          "またねー",
          "しね",
          "おまえなんてきらいだ",
          "東京ビックサイトはどっちですか?",
          "またねー",
          "しね",
          "おまえなんてきらいだ",
          "東京ビックサイトはどっちですか?",
          "またねー",
        ]
        for msg in test_msgs:
            self.assertIn(cre.dictMsg(msg), EXPECTED_REPLY_LIST)


if __name__ == "__main__":
    unittest.main()
