import os

from tornado.ioloop import IOLoop

from tornado_pytest.app import application


if __name__ == '__main__':
    application.listen(os.environ['APP_PORT'])
    ioloop = IOLoop.current()
    ioloop.start()

