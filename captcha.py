from PIL import Image, ImageDraw, ImageFont, ImageFilter
from base import BaseHandler
from hashlib import md5
from random import choice
from string import ascii_letters, digits


class Captcha:

    def __init__(self, signature):
        self.signature = md5(signature.encode("utf-8")).hexdigest()
        self.captcha = ''.join(choice(ascii_letters + digits) for _ in range(5).encode('utf-8'))
        self.pic = self.create_pic(size=(130, 30))

    def create_pic(self, size=(130, 30)):
        pic = Image.new('RGB', size, (255, 255, 255))
        draw = ImageDraw.Draw(pic)
        def gen_text():
            pass
        return 1


class CaptchaHandler(BaseHandler):

    pass
