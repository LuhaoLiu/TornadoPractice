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

    def has_permission(self, per_name):
        self.user = User(self.user.username)
        if self.user.permission is not None and self.user.permission.get(per_name) == 1:
            return True
        else:
            return False

    @authenticated
    def open(self):
        if self.has_permission("connect"):
            if list(map(lambda u: True if u.user.username == self.user.username else False, on_line_users)).count(True) == 0:
                on_line_users.append(self)
                data = dict(type='user', username=self.user.username, action='joined')
                self.send_all(data)
            else:
                data = dict(type="denied", permission="connect(Only one device at most)")
                self.write_message(json.dumps(data))
                self.close()
        else:
            data = dict(type="denied", permission="connect")
            self.write_message(json.dumps(data))
            self.close()

    def on_message(self, message):
        if self.has_permission("speak") and self.has_permission("connect"):
            data = dict(type='message', message=message, username=self.user.username)
            database.insert("ws_record", **{
                "uid": str(self.user.uid),
                "content": str(base64.b64encode(bytes(message, encoding='utf-8')), encoding='utf-8'),
                "date": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            })
            self.send_all(data)
        else:
            data = dict(type="denied", permission="speak")
            self.write_message(json.dumps(data))

    def on_close(self):
        data = dict(type='user', username=self.user.username, action='left')
        try:
            on_line_users.remove(self)
        except ValueError:
            pass
        else:
            self.send_all(data)

    def send_all(self, data):
        for user in on_line_users:
            user.write_message(json.dumps(data))
