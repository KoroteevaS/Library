#!/usr/local/bin/python3

from cgitb import enable 
enable()

from cgi import FieldStorage 
from os import environ
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie

result = ''
redirect =''
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if not http_cookie_header:
        sid = sha256(repr(time()).encode()).hexdigest()
        cookie['sid'] = sid
    else:
        cookie.load(http_cookie_header)
        sid = cookie['sid'].value

    session_store = open('sess_' + sid, writeback=True)

    # Get the id of the item being added to the cart
    form_data = FieldStorage()
    book_id = form_data.getfirst('book_id')
    qty = session_store.get(book_id)
    if not qty:
        qty = 1
    else:
        qty += 1
    session_store[book_id]=qty
    session_store.close()
    print(cookie)
    result = '<p>Book successfully added to your account.</p>'
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
    redirect ='<meta http-equiv="refresh" content="0;URL=\'index.py\'" >'

    
print('Content-Type: text/html')
print()

print("""<!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Shrine of Books</title>
            <link rel="stylesheet" href="library.css">
        </head>
        <body>
            %s
            <p>
                <a href="show_account.py">Show My Account</a>
            </p>
            <p>
                <a href="show_library.py">Show All the books</a>
            </p>
            %s
        </body>
     
    </html>""" % (result, redirect))
