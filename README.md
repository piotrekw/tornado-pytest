Testing Tornado applications with py.test (and requests)
========================================================

The following is a proof of concept for testing web applications written in Tornado with [py.test](http://pytest.org).

The problem
-----------

Testing applications written in Tornado is a piece of cake. The package provides a bunch of [handy tools](http://www.tornadoweb.org/en/stable/testing.html) for that, and in most cases that's all you need.

However, sometimes out-of-the-box tools are not enough. For instance, if you want to test a case where your handler responds with ``4xx`` status code. Or if the aplication you're testing is using cookies. It is particularly uncomfortable to test such cases with ``tornado.testing``.

Don't you think it would be great to accomplish this with a clean and elegant interface like [requests](http://docs.python-requests.org/en/latest/)?

The solution
------------

Good news: it is possible with py.test and [xprocess](https://pypi.python.org/pypi/pytest-xprocess) plugin. Just have a look at the code below:

```python
@pytest.fixture(scope='session')
def test_server(xprocess, request):
  def preparefunc(cwd):
    def check_port():
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      for i in xrange(10):
        result = sock.connect_ex(('127.0.0.1', TEST_APP_PORT))
        if result == 0:
          return True
        time.sleep(1)
      return False
      
    os.environ['APP_PORT'] = str(TEST_APP_PORT)
    server_path = os.path.join(sys.prefix, 'bin', 'tornado_pytest_app.py')
    return (check_port, [sys.executable, server_path])
    
  pid, log = xprocess.ensure('tornado_pytest_app', preparefunc, restart=True)
  
  def fin():
    os.kill(pid, signal.SIGKILL)
  request.addfinalizer(fin)

  def get_url(url):
    return 'http://localhost:%s%s' % (TEST_APP_PORT, url)

  return get_url
```

The fixture above does a few simple things:

1. Runs you application in a subprocess.
2. Waits until the application starts (the ``check_port`` function).
3. Kills the application once the fixture is finalized.
4. Returns ``get_url`` function, which you can use to get a URL for the test server.
