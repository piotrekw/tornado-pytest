from distutils.core import setup

setup(
    name='Tornado-py.test',
    version='1.0',
    description='Testing Tornado applications with py.test',
    author='Piotr Wasilewski',
    author_email='piotrek@piotrek.io',
    packages=['tornado_pytest'],
    scripts=['tornado_pytest/bin/tornado_pytest_app.py']
)
