from tornado.web import RequestHandler
from base import info_load_from_json, info_write_in_json
from os import path


class SetupHandler(RequestHandler):

    def get(self):
        mysql_info = {
            "mysql_host": "localhost",
            "mysql_port": "3306",
            "mysql_user": "ws_admin",
            "mysql_password": "Default_PWD0",
            "database_name": "ws"
        }
        server_info = {
            "port": "2333",
            "cookie_secret": "**TODO:GENERATE_YOUR_COOKIE_SECRET**"
        }
        try:
            mysql_info.update(info_load_from_json(path.join(path.realpath(path.dirname(__file__)), "info/mysql.json")))
            server_info.update(info_load_from_json(path.join(path.realpath(path.dirname(__file__)), "info/server.json")))
        except:
            self.render("template/setup.html", mysql_info=mysql_info, server_info=server_info)
        else:
            self.render("template/setup.html", mysql_info=mysql_info, server_info=server_info)

    def post(self):
        info = self.request.body_arguments
        print(info)
