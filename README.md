# mahjong-line-bot
麻雀なかまをあつめて麻雀を始めるボット

## ちょっとした説明
`app.py`　lineからのメッセージを受けて返信するサーバーが立ち上がる。
`create_reply.py` 返信メッセージを作成するclassなどがある。今はMahjongGoクラスがあるだけなので名前がよくない気もする。

## 補足
herokで運用している。
もろもろのファイルはherok用のもの
httpsでSSL証明がないと(ちゃんとした外部にあるサーバー)LINE からのリクエストを受けられず、
自宅のPCだと動かすのが面倒だから。
まともなテストもローカルだとできない。
