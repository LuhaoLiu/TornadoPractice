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
        data = dict(type='user', username=self.user.username, action='joined')
        self.send_all(data)

    def on_message(self, message):
        data = dict(type='message', message=message, username=self.user.username)
        database.insert("ws_record", **{
            "uid": str(self.user.uid),
            "content": str(base64.b64encode(bytes(message, encoding='utf-8')), encoding='utf-8'),
            "date": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        })
        self.send_all(data)

    def on_close(self):
        on_line_users.remove(self)
        data = dict(type='user', username=self.user.username, action='left')
        self.send_all(data)

    def send_all(self, data):
        for user in on_line_users:
            user.write_message(json.dumps(data))
