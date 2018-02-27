from tornado.web import RequestHandler
from base import info_load_from_json, info_write_in_json
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
            database = pymysql.connect(host=str(mysql_info.get("mysql_host")),
                                       port=int(mysql_info.get("mysql_port")),
                                       user=str(mysql_info.get("mysql_user")),
                                       passwd=str(mysql_info.get("mysql_password")),
                                       database=str(mysql_info.get("database_name")))
        except:
            self.render("template/setup.html", mysql_info=mysql_info, server_info=server_info,
                        warn="Unable to connect to the database")
        else:
            cursor = database.cursor()
            create_table_sql = """CREATE TABLE IF NOT EXISTS ws_account(
                              uid      INT UNSIGNED AUTO_INCREMENT
                              PRIMARY KEY,
                              username VARCHAR(25) NOT NULL,
                              email    VARCHAR(50) NOT NULL,
                              password VARCHAR(64) NOT NULL,
                              reg_time DATETIME    NOT NULL,
                              session  VARCHAR(64) NULL,
                              CONSTRAINT username
                              UNIQUE (username),
                              CONSTRAINT email
                              UNIQUE (email)
                              )ENGINE = InnoDB DEFAULT CHARSET=utf8;"""
            cursor.execute(create_table_sql)
            create_table_sql = """CREATE TABLE IF NOT EXISTS ws_permission(
                              uid     INT UNSIGNED AUTO_INCREMENT
                              PRIMARY KEY,
                              speak   TINYINT(1) DEFAULT '1' NOT NULL,
                              connect TINYINT(1) DEFAULT '1' NOT NULL,
                              gag     TINYINT(1) DEFAULT '0' NOT NULL,
                              root    TINYINT(1) DEFAULT '0' NOT NULL,
                              admin   TINYINT(1) DEFAULT '0' NOT NULL,
                              CONSTRAINT ws_permission_ws_account_uid_fk
                              FOREIGN KEY (uid) REFERENCES ws_account (uid)
                              )ENGINE = InnoDB DEFAULT CHARSET=utf8;"""
            cursor.execute(create_table_sql)
            create_table_sql = """CREATE TABLE IF NOT EXISTS ws_record(                                
                              id      BIGINT UNSIGNED AUTO_INCREMENT
                              PRIMARY KEY,
                              uid     INT UNSIGNED NOT NULL,
                              content TEXT         NOT NULL,
                              date    DATETIME     NULL,
                              CONSTRAINT ws_record_ws_account_uid_fk
                              FOREIGN KEY (uid) REFERENCES ws_account (uid)
                              )ENGINE = InnoDB DEFAULT CHARSET=utf8;"""
            cursor.execute(create_table_sql)
            create_table_sql = """CREATE INDEX ws_record_ws_account_uid_fk ON ws_record (uid);"""
            cursor.execute(create_table_sql)
            database.commit()
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

