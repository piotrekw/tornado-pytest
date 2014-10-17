import os
import signal
import socket
import sys
import time

import pytest


TEST_APP_PORT = 5050


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

