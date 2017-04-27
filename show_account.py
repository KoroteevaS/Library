#!/usr/local/bin/python3

from cgitb import enable 
enable()

from os import environ
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db

result = ''
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if  http_cookie_header:
        cookie.load(http_cookie_header)
        cookie['sid']['expires']=157680000
        sid = cookie['sid'].value
        session_store = open('sess_' + sid, writeback=True)
        if 'authenticated' in session_store:
            if session_store['authenticated'] == False:
                result ='<p class = "warn"> You have to be logged in </p>'
            else:
                if len(session_store) == 0:
                    result = '<p>No books on your shelf.</p>'
                else:
                    try:
                        connection = db.connect('cs1dev.ucc.ie', 'sy1',  'gaequaez', 'csdipact2015_1_sy1')
                        cursor = connection.cursor(db.cursors.DictCursor)
                        result = """<table id = "account">
                           <tr><td colspan="2"><H2>My Book Shelf</H2></td></tr>"""
                        for book_id in session_store:
                            cursor.execute("""SELECT book_name, author, book_link, images FROM library
                               WHERE book_id = %s""", (book_id))
                            for row in cursor.fetchall():
                                result += """<tr><td>%s, </td><td>%s</td></tr><br><tr><td colspan = "2"><a href = %s><img src = %s alt ="bookcover" width = "200"></a></td></tr><br>""" %(row['book_name'], row['author'], row['book_link'], row['images'])
                            result += "</table>"
                        cursor.close()  
                        connection.close()
                    except db.Error as err:
                        result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

            session_store.close()
            print(cookie)
        else:
            result ='<p class = "warn"> You have to be logged in to see this page</p>'
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
    
    
print('Content-Type: text/html')
print()
print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Shrine of Books</title>
            <link rel="stylesheet" href="library.css">
        </head>
        <body>
            <div id = shelf>
            %s
            </div>
           <ul>
             <li><a href="show_library.py">Show All The Books</a></li>
             <li><a href="login.py">Press to login.</a></li>
             <li><a href="index.py"><---Go to the main page</a></li>
           </ul>
        </body>
    </html>""" % (result))

