from base import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        self.get_current_user()
        self.render("template/index.html", user=self.user)
