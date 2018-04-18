import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
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
