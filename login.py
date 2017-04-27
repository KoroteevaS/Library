#!/usr/local/bin/python3

from cgitb import enable 
enable()

from cgi import FieldStorage, escape
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db

form_data = FieldStorage()
username = ''
result = ''
if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password = escape(form_data.getfirst('password', '').strip())
    if not username or not password:
        result = '<p>Error: user name and password are required</p>'
    else:
        sha256_password = sha256(password.encode()).hexdigest()
        try:
            connection = db.connect('cs1dev.ucc.ie', 'sy1',  'gaequaez', 'csdipact2015_1_sy1')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users 
                              WHERE username = %s
                              AND password = %s""", (username, sha256_password))
            if cursor.rowcount == 0:
                result = '<p>Error: incorrect user name or password</p>'
            else:
                cookie = SimpleCookie()
                sid = sha256(repr(time()).encode()).hexdigest()
                cookie['sid'] = sid
                cookie['sid']['expires']=157680000
                session_store = open('sess_' + sid, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = username
                session_store.close()
                result = """
                   <p>Succesfully logged in!</p>
                   <p>Welcome back to our Library</p>
                   <ul>
                       <li><a href="upload.py">You may upload files</a></li>
                       <li><a href = "comments.py">You may write comments</li>
                       <li><a href="logout.py">Logout</a></li>
                   </ul>"""
                print(cookie)
            cursor.close()  
            connection.close()
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
        
print('Content-Type: text/html')
print()
print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Login to Library</title>
            <LINK rel="stylesheet" href="library.css">
        </head>
        <body>
            <form action="login.py" method="post">
            
                <label for="username">User name: </label>
                <input type="text" name="username" id="username" value="%s"><br>
                <label for="password">Password: </label>
                <input type="password" name="password" id="password"><br>
                <input type="submit" value="Login">
            </form>
            %s
            <a href="index.py"><---Go to the main page</a>
        </body>
    </html>""" % (username, result))
