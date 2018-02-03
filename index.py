from base import BaseHandler
from tornado.web import authenticated


class IndexHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render("template/index.html", user=self.user)
