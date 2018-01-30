from base import BaseHandler
from tornado.web import authenticated


class IndexHandler(BaseHandler):

    @authenticated
    def get(self):
        username = self.user.username
        page = {
            "login": "Chick to login again",
            "logout": "Chick to logout",
            "register": "Chick to Register",
            "/": "Click to go to the index",
            "chat": "Chick to go to the chat room",
            "/user/" + username: "Chick to go to the personal page"
        }
        self.render("template/index.html",
                    user=self.user,
                    urls=page)
