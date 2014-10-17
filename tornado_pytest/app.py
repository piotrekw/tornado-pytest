from tornado.web import url, Application, RequestHandler


class Handler(RequestHandler):
    def get(self):
        self.write({'status': 'ok'})
        self.finish()


application = Application([url(r'/', Handler)])

