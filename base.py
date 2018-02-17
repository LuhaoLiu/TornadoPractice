from tornado.web import RequestHandler
from re import match
from os import path
import pymysql
import json


def has_user(username, email):
    username_uid = database.query("ws_account", "uid", "username = '%s'" % username)
    email_uid = database.query("ws_account", "uid", "email = '%s'" % email)

    if username_uid == () and email_uid == ():
        return False, '', '', 'fail'
    elif username_uid == () and email_uid != ():
        return True, '', 'email', 'fail'
    elif username_uid != () and email_uid == ():
        return True, 'username', '', 'fail'
    elif username_uid != () and email_uid != ():
        if username_uid == email_uid:
            return True, 'username', 'email', 'success'
        else:
            return True, 'username', 'email', 'fail'


def username_check(username):
    if len(username) > 22 or len(username) < 5:
        raise TypeError("The length of username must be over 5 and under 15")
    elif not match("^[0-9a-zA-Z_]+$", username):
        raise TypeError("Username contains illegal characters")
    else:
        return 'valid'


def email_check(email):
    if (not match("^[0-9a-zA-Z_\.-]+@[0-9a-zA-Z_-]+\.[0-9a-zA-Z\._-]+$", email)) or len(email) > 45:
        raise TypeError("The email address is invalid or too long")
    else:
        return 'valid'


def info_load_from_json(path):
    f = open(path)
    info = json.load(f)
    f.close()
    return info


class Database:

    def __init__(self, database):
        self.database = database

    def query(self, table_name, select='*', where='true'):
        query_sql = """SELECT %s FROM %s WHERE %s;""" % (select, table_name, where)
        self.database.commit()
        cursor = self.database.cursor()
        cursor.execute(query_sql)
        fetchall = cursor.fetchall()
        cursor.close()
        return fetchall

    def insert(self, table_name, **values):
        insert_sql = """INSERT INTO %s(""" % table_name
        for column in values:
            insert_sql += (column + ', ')
        insert_sql = insert_sql[0:len(insert_sql) - 2]
        insert_sql += ') VALUES ('
        for value in values:
            insert_sql += ("'" + values[value] + "', ")
        insert_sql = insert_sql[0:len(insert_sql) - 2]
        insert_sql += ');'
        cursor = self.database.cursor()
        cursor.execute(insert_sql)
        self.database.commit()
        cursor.close()

    def update(self, table_name, values, where):
        update_sql = """UPDATE %s SET """ % table_name
        for key in values:
            update_sql += """%s='%s', """ % (key, values[key])
        update_sql = update_sql[0:len(update_sql) - 2]
        update_sql += """ WHERE %s;""" % where
        cursor = self.database.cursor()
        cursor.execute(update_sql)
        self.database.commit()
        cursor.close()

    def delete(self, table_name, where):
        delete_sql = """DELETE FROM %s WHERE %s;""" % (table_name, where)
        cursor = self.database.cursor()
        cursor.execute(delete_sql)
        self.database.commit()
        cursor.close()

    def close(self):
        self.database.close()


database_info = info_load_from_json(path.join(path.realpath(path.dirname(__file__)), "info", "mysql.json"))
database = Database(pymysql.connect(host=str(database_info.get("mysql_host")),
                                    port=int(database_info.get("mysql_port")),
                                    user=str(database_info.get("mysql_user")),
                                    passwd=str(database_info.get("mysql_password")),
                                    database=str(database_info.get("database_name"))))


def close_database():
    global database
    database.close()


class User:

    def __init__(self, username):
        self.username = username
        self.email = None
        self.uid = None
        self.reg_time = None
        self.permission = None
        self.get_information()

    def get_information(self):
        if username_check(self.username) == 'valid':
            result = database.query("ws_account", "email,uid,reg_time,username", "username = '%s'" % self.username)
            if result != ():
                self.email = result[0][0]
                self.uid = int(result[0][1])
                self.reg_time = result[0][2]
                self.username = result[0][3]
                permission = database.query("ws_permission", "*", "uid = '%s'" % self.uid)
                if permission is not None:
                    self.permission = dict(speak=permission[0][1],
                                           connect=permission[0][2],
                                           gag=permission[0][3],
                                           delete=permission[0][4],
                                           root=permission[0][5],
                                           admin=permission[0][6])


class BaseHandler(RequestHandler):

    def get_current_user(self):
        self.user = None
        if self.get_secure_cookie("session_id") is None:
            return None
        else:
            session_id = str(self.get_secure_cookie("session_id"), encoding='utf-8')
        username = database.query("ws_account",
                                  "username",
                                  "session='%s'" % session_id)
        if username == ():
            return None
        else:
            self.user = User(username[0][0])
            return self.user

    def get(self):
        self.write_error(404)

    def write_error(self, status_code, info='', **kwargs):
        self.get_current_user()
        self.render("template/error.html", status_code=status_code, info=info, user=self.user)
