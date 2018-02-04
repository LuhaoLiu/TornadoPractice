from base import BaseHandler
from tornado.web import authenticated
from base import database, has_user, email_check, username_check
from hashlib import sha256
from random import randint, choice
from string import ascii_letters, digits
import time


class LoginHandler(BaseHandler):

    def get(self):
        if self.get_current_user() is not None:
            self.render("template/warn.html",
                        information=r'You have already been logged in<br />'
                                    r'Please <a href="logout?next=/login">logout</a> at first',
                        title="Warn",
                        user=self.user)
        else:
            self.render("template/login.html", text=None, default=dict(user=''))

    def post(self):
        if '@' in self.get_argument("user"):
            user = self.get_argument("user")
            try:
                email_check(user)
            except TypeError as err:
                self.render("template/login.html",
                            text=err,
                            default=dict(user=user))
                return
            else:
                real_pwd = database.query("ws_account", "password", "email='%s'" % user)
                username = database.query("ws_account", "username", "email='%s'" % user)
                if username != ():
                    username = username[0][0]
                email = user
        else:
            user = self.get_argument("user")
            try:
                username_check(user)
            except TypeError as err:
                self.render("template/login.html",
                            text=err,
                            default=dict(user=user))
                return
            else:
                real_pwd = database.query("ws_account", "password", "username='%s'" % user)
                email = database.query("ws_account", "email", "username='%s'" % user)
                if email != ():
                    email = email[0][0]
                username = user
        pwd = self.get_argument("password")
        if real_pwd == () or str(real_pwd[0][0]) != str(sha256(pwd.encode('utf-8')).hexdigest()) or len(pwd) < 8:
            self.render("template/login.html",
                        text="User do not exist or invalid password",
                        default=dict(user=user))
        elif str(real_pwd[0][0]) == str(sha256(pwd.encode('utf-8')).hexdigest()):
            random_string = ''.join(choice(ascii_letters + digits) for _ in range(randint(5, 20))).encode('utf-8')
            if self.get_argument("remember", default=None) is None:
                if randint(0, 1):
                    session_id = str(sha256(username.encode('utf-8') + random_string).hexdigest())
                    database.update("ws_account", dict(session=session_id), "username='%s'" % username)
                    database.insert("ws_account", )
                    self.set_secure_cookie("session_id", value=session_id, expires_days=1)
                else:
                    session_id = str(sha256(email.encode('utf-8') + random_string).hexdigest())
                    database.update("ws_account", dict(session=session_id), "username='%s'" % username)
                    self.set_secure_cookie("session_id", value=session_id, expires_days=1)
            else:
                if randint(0, 1):
                    session_id = str(sha256(username.encode('utf-8') + random_string).hexdigest())
                    database.update("ws_account", dict(session=session_id), "username='%s'" % username)
                    self.set_secure_cookie("session_id", value=session_id, expires_days=30)
                else:
                    session_id = str(sha256(email.encode('utf-8') + random_string).hexdigest())
                    database.update("ws_account", dict(session=session_id), "username='%s'" % username)
                    self.set_secure_cookie("session_id", value=session_id, expires_days=30)
            self.redirect(r"/" if str(self.get_argument("next", default=r"/"))[0:7] == r"/logout" or
                                  str(self.get_argument("next", default="/"))[0:6] == "logout"
                          else str(self.get_argument("next", default="/")))


class RegisterHandler(BaseHandler):

    def get(self):
        if self.get_current_user() is not None:
            self.render("template/warn.html",
                        information=r'You have already been logged in<br />'
                                    r'Please <a href="logout?next=/register">logout</a> at first',
                        title="Warn",
                        user=self.user)
        else:
            self.render("template/register.html", text=None, default=dict(email='', username=''))

    def post(self):
        username = str(self.get_argument("username"))
        email = str(self.get_argument("email"))
        pwd = str(self.get_argument("pwd"))
        try:
            username_check(username)
            email_check(email)
        except TypeError as err:
            self.render("template/register.html",
                        text=err,
                        default=dict(email=email, username=username))
        else:
            if len(pwd) < 8:
                self.render("template/register.html",
                            text="The length of the password must over 8",
                            default=dict(email=email, username=username))
            else:
                result = has_user(username, email)
                if result[0]:
                    if result[3] == 'success':
                        self.render("template/register.html",
                                    text="This user has already been existed",
                                    default=dict(email=email, username=username))
                    else:
                        if result[1] != '' and result[2] != '':
                            text = "This username and email have been used"
                        elif result[1] != '':
                            text = "This username has been used"
                        elif result[2] != '':
                            text = "This email has benn used"
                        self.render("template/register.html",
                                    text=text,
                                    default=dict(email=email, username=username))
                else:
                    database.insert("ws_account", **{"username": username,
                                                     "email": email,
                                                     "password": str(sha256(pwd.encode('utf-8')).hexdigest()),
                                                     "reg_time": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))})
                    self.render("template/warn.html",
                                information=r'You have already successfully registered<br />'
                                            r'Chick <a href="/login">here</a> to login',
                                title="Remind",
                                user=None)


class LogoutHandler(BaseHandler):

    @authenticated
    def get(self):
        self.clear_cookie("session_id")
        self.redirect(str(self.get_argument("next", default="/")))
