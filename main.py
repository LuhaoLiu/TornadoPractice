from tornado.web import Application
from tornado.ioloop import IOLoop
from base import BaseHandler, database
from index import IndexHandler
from confirm import LoginHandler, LogoutHandler, RegisterHandler
from account import UserHandler
from webscoket import WSServerHandler, WSUserHandler
from os import path


settings = dict(
    cookie_secret="a02i%fJIi28HI398ufTf$u84)91n^d2N",
    login_url=r"/login",
    autoreload=True,
    static_path=path.join(path.realpath(path.dirname(__file__)), "static"),
    xsrf_cookies=True,
    default_handler_class=BaseHandler)


def make_app():
    return Application([
        (r"/", IndexHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/register", RegisterHandler),
        (r"/user/([0-9a-zA-Z_]+)", UserHandler),
        (r"/chat", WSUserHandler),
        (r"/ws", WSServerHandler)
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(2333)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        database.close()
        print("Server and database connection have already closed.")
