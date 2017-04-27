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
    password1 = escape(form_data.getfirst('password1', '').strip())
    password2 = escape(form_data.getfirst('password2', '').strip())
    if not username or not password1 or not password2:
        result = '<p>Error: user name and passwords are required</p>'
    elif password1 != password2:
        result = '<p>Error: passwords must be equal</p>'
    else:
        try:
            connection = db.connect('cs1dev.ucc.ie', 'sy1',  'gaequaez', 'csdipact2015_1_sy1')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users 
                              WHERE username = %s""", (username))
            if cursor.rowcount > 0:
                result = '<p>Error: user name already taken</p>'
            else:
                sha256_password = sha256(password1.encode()).hexdigest()
                cursor.execute("""INSERT INTO users (username, password) 
                                  VALUES (%s, %s)""", (username, sha256_password))
                connection.commit()
                cursor.close()  
                connection.close()
                cookie = SimpleCookie()
                sid = sha256(repr(time()).encode()).hexdigest()
                cookie['sid'] = sid
                session_store = open('sess_' + sid, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = username
                session_store.close()
                result = """
                   <p>Succesfully inserted!</p>
                   <p>Thank you for joining us</p>
                   <ul>
                       <li><a href="show_account.py">Show my account</a></li>
                       <li><a href="index.py">Go to the main page</a></li> 
                       <li><a href="logout.py">Logout</a></li>
                   </ul>"""
                print(cookie)
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
        
print('Content-Type: text/html')
print()
print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Library</title>
            <LINK rel="stylesheet" href="library.css">
        </head>
        <body>
            <form action="register.py" method="post">
                <label for="username">User name: </label>
                <input type="text" name="username" id="username" value="%s"><br>
                <label for="password1">Password: </label>
                <input type="password" name="password1" id="password1"><br>
                <label for="passwords2">Re-enter password: </label>
                <input type="password" name="password2" id="password2"><br>
                <input type="submit" value="Register">
            </form>
            %s
        </body>
    </html>""" % (username, result))
