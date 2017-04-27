#!/usr/local/bin/python3
from cgitb import enable 
enable()

from cgi import FieldStorage, escape
import pymysql as db
from os import environ
from shelve import open
from http.cookies import SimpleCookie
import datetime


print('Content-Type: text/html')
print()

comments = ''
now = datetime.datetime.now()
message = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second )
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if not http_cookie_header:
        comments ='<p class="warn"> You are not logged in at all </p><a href = login.py>Click here to log in.</a>'
    else:
        cookie.load(http_cookie_header)
        if 'sid' in http_cookie_header:
            sid = cookie['sid'].value
            session_store = open('sess_' + sid, writeback=True)
            try:
                connection = db.connect('cs1dev.ucc.ie', 'sy1',  'gaequaez', 'csdipact2015_1_sy1')
                cursor = connection.cursor(db.cursors.DictCursor)
                form_data = FieldStorage()
                username = form_data.getfirst('username')
                new_comment = form_data.getfirst('new_comment')
                if 'authenticated' in session_store:
                    if session_store['authenticated'] == True:
                        if len(form_data) != 0:   
                            if username != None:
                                if new_comment != None:
                                    cursor.execute("""INSERT INTO comments_table (username, comment, today_date)
                                      VALUES (%s, %s,%s)""", (username, new_comment, message))
                                    connection.commit()
                                else:
                                    comments = "Enter text"
                            else:
                                comments = "Enter your name"
                        else:
                            comments= '<p class = "warn"> You need to be logged in to write the comments</p><a href = login.py>Click here to log in.</a>'
                    else:
                        comments= '<p class = "warn"> You need to be logged in to write the comments</p><a href = login.py>Click here to log in.</a>'                
                cursor.execute("""SELECT * FROM comments_table 
                       ORDER BY comment_id DESC""")
                for row in cursor.fetchall(): 
                    comments += '<article><h3>%s</h3><p>%s</p><p class = "small">%s</p></article>' % (row['username'], row['comment'], row['today_date'])
                cursor.close()  
                connection.close()
            except db.Error:
                comments = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
      
except IOError:
    result ='<p> We are experiencing problems at the moment. Please call back later.</p>'
print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Library - Comments</title>
            <link rel="stylesheet" href="library.css">
        </head>
        <body>
           <h2>Comments</h2>
              <section>
                <form action="comments.py" method="post">
                    <fieldset class="form">
                        <legend>Post a new comment</legend>
                        <label for="username">Name:</label>
                        <input type="text" name="username" id="username"><br>
                        <label for="new_comment">Comment:</label>
                        <textarea name="new_comment" id="new_comment" rows="5" cols="50">
                        </textarea><br>
                        <input type="submit" value = "Submit Comment">
                    </fieldset>
                </form>
                 <a class="small" href = 'index.py'><---Go to the main page</a>
                %s
            </section>
        </body>
    </html>""" % (comments))
        
