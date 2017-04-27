#!/usr/local/bin/python3

from cgitb import enable
enable()

import pymysql as db

from os import environ
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie

print('Content-Type: text/html')
print()

result = ''
links = ''
flag = False

try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    
    if  http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in http_cookie_header:
            sid = cookie['sid'].value
            session_store = open('sess_' + sid, writeback=True)
            if 'authenticated' in session_store:
                if session_store['authenticated'] == True:
                    try:
                        connection = db.connect('cs1dev.ucc.ie', 'sy1',  'gaequaez', 'csdipact2015_1_sy1')
                        cursor     = connection.cursor(db.cursors.DictCursor)
                        cursor.execute("""SELECT * FROM library ORDER BY book_id""")
                        result = """<table cellspacing="10" >
                                <tr><td colspan = '3' ><h1>All Books</h1></td></tr>
                                <tr><th> Name </th><th> Author </th><th> Year </th><th></th></tr>"""
                        for row in cursor.fetchall():
                            result += """<tr>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s </td>
                            <td><a  class = "small" href="add_to_account.py?book_id=%s">Add to read</a></td>
                            </tr>""" % (row['book_name'], row['author'], row['written'], row['book_id'])
                        result += '</table>'
                        flag = True
                        cursor.close()  
                        connection.close()
                        links = '<li><a href="show_account.py">Show my account.</a></li>'
                    except db.Error:
                        result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'


if not flag:
    try:
        connection = db.connect('cs1dev.ucc.ie', 'sy1',  'gaequaez', 'csdipact2015_1_sy1')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT * FROM library ORDER BY book_id""")
        result = """<table>
                   <tr><td><h1>All Books</h1></tr>
                    <tr><th>Name</th><th>Author</th></tr>"""
        for row in cursor.fetchall():
            result += """<tr>
                    <td>%s</td>
                    <td>%s</td>
                    </tr>""" % (row['book_name'], row['author'])
        result += '</table>'
        cursor.close()
        connection.close()
    except db.Error:
        result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
print(  """<!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Shrine of Books</title>
            <link rel="stylesheet" href="library.css">
        </head>
        <body>
            %s
             <ul>            
                %s
                <li><a href="index.py">Go to the main page.</a></li>
              </ul>
        </body>
    </html>""" % (result, links))


