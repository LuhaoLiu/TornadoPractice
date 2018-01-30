from base import database, BaseHandler, User
from tornado.websocket import WebSocketHandler
from tornado.web import authenticated
import base64
import time
import json


on_line_users = []


class WSUserHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render("template/webscoket.html", username=self.user.username)


class WSServerHandler(WebSocketHandler, BaseHandler):

    def open(self):
        self.user = self.get_current_user()
        on_line_users.append(self)

    def on_message(self, message):
        data = dict(message=message, username=self.user.username, encoding='utf-8')
        database.insert("ws_record", **{
            "uid": str(self.user.uid),
            "content": str(base64.b64encode(bytes(message, encoding='utf-8')), encoding='utf-8'),
            "date": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        })
        for user in on_line_users:
            user.write_message(json.dumps(data))

    def on_close(self):
        on_line_users.remove(self)

