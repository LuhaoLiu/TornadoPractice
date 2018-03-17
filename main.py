from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from base import BaseHandler, info_load_from_json, database
from index import IndexHandler
from confirm import LoginHandler, LogoutHandler, RegisterHandler
from user import UserHandler
from webscoket import WSServerHandler, WSUserHandler
from setup import SetupHandler
from os import path


settings = dict(
    cookie_secret="DEFAULT",
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


def make_setup_app():
    return Application([
        (r"/.*", SetupHandler)
    ], static_path=path.join(path.realpath(path.dirname(__file__)), "static"))


if __name__ == "__main__":
    if database is not None:
        print("Database successfully connected.")
        try:
            server_info = info_load_from_json(path.join(path.realpath(path.dirname(__file__)), "info", "server.json"))
            settings.update(cookie_secret=server_info.get("cookie_secret"))
            app = make_app()
            server = HTTPServer(app)
            server.listen(server_info.get("port"))
            print("Server successfully started.")
        except Exception as e:
            print(e)
            app = make_setup_app()
            server = HTTPServer(app)
            server.listen(8080)
    else:
        print("Server successfully started.")
        app = make_setup_app()
        server = HTTPServer(app)
        server.listen(8080)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        if database is not None:
            database.close()
            print("Server and database connection have already closed.")
        else:
            print("Server have already closed.")
