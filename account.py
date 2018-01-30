from base import BaseHandler, User
from tornado.web import authenticated

class UserHandler(BaseHandler):

    @authenticated
    def get(self, username):
        user = User(username)
        if user.uid is None:
            self.write_error(404, "User not found")
        else:
            self.render("template/user.html", user=user)
