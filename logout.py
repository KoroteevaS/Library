#!/usr/local/bin/python3

from cgitb import enable 
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie

print('Content-Type: text/html')
print()

result = ''
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if not http_cookie_header:
        result = '<p>You are already logged out</p>'
    else:
        cookie.load(http_cookie_header)
        sid = cookie['sid'].value
        session_store = open('sess_' + sid, writeback=True)
        session_store['authenticated'] = False
        session_store.close()
        result = """
            <p>You are now logged out. Thanks for using our library</p>
            <p><a href="login.py">Login again</a></p>
            <p><a href="index.py"><---Go to the main page</a></p>"""
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Library</title>
            <LINK rel="stylesheet" href="library.css">
        </head>
        <body>
            %s
        </body>
    </html>""" % (result))

