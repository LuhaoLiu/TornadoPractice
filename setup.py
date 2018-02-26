from tornado.web import RequestHandler
from base import info_load_from_json, info_write_in_json, Database
from os import path
import pymysql


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
            self.render("template/setup.html", mysql_info=mysql_info, server_info=server_info, warn=None)
        else:
            self.render("template/setup.html", mysql_info=mysql_info, server_info=server_info, warn=None)

    def post(self):
        info = self.request.body_arguments
        mysql_info = {
            "mysql_host": str(info.get("mysql_host")[0], encoding="utf-8"),
            "mysql_port": int(info.get("mysql_port")[0]),
            "mysql_user": str(info.get("mysql_user")[0], encoding="utf-8"),
            "mysql_password": str(info.get("mysql_password")[0], encoding="utf-8"),
            "database_name": str(info.get("database_name")[0], encoding="utf-8")
        }
        server_info = {
            "port": int(info.get("port")[0]),
            "cookie_secret": str(info.get("cookie_secret")[0], encoding="utf-8")
        }
        try:
            database = Database(pymysql.connect(host=str(mysql_info.get("mysql_host")),
                                                port=int(mysql_info.get("mysql_port")),
                                                user=str(mysql_info.get("mysql_user")),
                                                passwd=str(mysql_info.get("mysql_password")),
                                                database=str(mysql_info.get("database_name"))))
        except:
            self.render("template/setup.html", mysql_info=mysql_info, server_info=server_info,
                        warn="Unable to connect to the database")
        else:
            database.close()
            info_write_in_json(path.join(path.realpath(path.dirname(__file__)), "info/mysql.json"),
                               mysql_info)
            info_write_in_json(path.join(path.realpath(path.dirname(__file__)), "info/server.json"),
                               server_info)
            self.write("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Succeed</title>
                <link type="text/css" rel="stylesheet" href="static/css/default.css" />
            </head>
            <body>
                <div class="info_block">
                    <h1>Configuration is effective<br />Please restart the server manually</h1>
                </div>
            </body>
            </html>
            """)

