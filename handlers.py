
import tornado.ioloop
import tornado.web
import tornado.httpclient

import json
import redis
from log import MyLogger


class CommandHandler(tornado.web.RequestHandler):

    def initialize(self, *args, **kwargs):
        self.r = redis.Redis()
        self.command_key = "proxy_command"
        self.log = MyLogger()

    def get(self, *args, **kwargs):
        self.log.info("before rpop", self.command_key)
        command = self.r.rpop(self.command_key)
        self.log.info("after rpop", self.command_key)
        if not command:
            self.write(json.dumps({
                'code': -1,
                'error': "There are no commands.",
            }))
        else:
            self.write(json.dumps({
                'code': 0,
                'command': command.decode(),
            }))

    def post(self, *args, **kwargs):
        command = self.get_argument('command', None)
        if command:
            self.log.info("before lpush", self.command_key, command)
            self.r.lpush(self.command_key, command)
            self.log.info("after lpush", self.command_key, command)
            self.write(json.dumps({
                'code': 0,
                'data': 0,
            }))
        else:
            self.write(json.dumps({
                'code': -1,
                'data': -1,
            }))



class ReturnHandler(tornado.web.RequestHandler):

    def initialize(self, *args, **kwargs):
        self.r = redis.Redis()
        self.return_key = "proxy_return"
        self.log = MyLogger()

    def get(self, *args, **kwargs):
        self.log.info("before rpop", self.return_key)
        ret = self.r.rpop(self.return_key)
        self.log.info("after rpop", self.return_key)
        if not ret:
            self.write(json.dumps({
                'code': -1,
                'error': "There are no returns.",
            }))
        else:
            self.write(json.dumps({
                'code': 0,
                'return': ret.decode(),
            }))

    def post(self, *args, **kwargs):
        ret = self.get_argument("return", None)
        if ret:
            self.log.info("before lpush", self.return_key, ret)
            self.r.lpush(self.return_key, ret)
            self.log.info("after lpush", self.return_key, ret)
            self.write(json.dumps({
                'code': 0,
                'data': 0,
            }))
        else:
            self.write(json.dumps({
                'code': -1,
                'data': -1,
            }))

