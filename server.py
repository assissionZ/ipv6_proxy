import tornado.ioloop
import tornado.web
from tornado.options import define, options

from handlers import CommandHandler, ReturnHandler

urls = [
    (r"/command$", CommandHandler),
    (r"/return$", ReturnHandler),
]


class Application(tornado.web.Application):
    def __init__(self, handlers):
        tornado.web.Application.__init__(self, handlers)


if __name__ == "__main__":
    define("port", default=12345, help="run on the given port", type=int)
    options.parse_command_line()
    app = Application(urls)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
