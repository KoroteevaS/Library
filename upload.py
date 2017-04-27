#!/usr/local/bin/python3
import cgi, os
import cgitb; cgitb.enable()
from cgi import FieldStorage, escape
import pymysql as db
from http.cookies import SimpleCookie
from os import environ
from shelve import open


print('Content-Type: text/html')
print()

form_data = FieldStorage()
result = ''
savefile = ''
book_name = ''
book_link =''
images = ''
author = ''
year   = ''
answer = ''
book_msg =''
author_msg =''
year_msg = ''
file_txt_msg = ''
file_img_msg = ''
file1 = ''
file2 = ''

if len(form_data) !=0:
    try:
         connection = db.connect('cs1dev.ucc.ie', 'sy1',  'gaequaez', 'csdipact2015_1_sy1')
         cursor = connection.cursor(db.cursors.DictCursor)
         bookname = escape(form_data.getfirst('bookname', "").strip())
         author = escape(form_data.getfirst('author', "").strip())
         year   = escape(form_data.getfirst('year', "").strip())
         book_link = escape(form_data.getfirst('book_link', "").strip())
         images = escape(form_data.getfirst('images', "").strip())
         cursor.execute("Insert INTO library (book_name, author, written, book_link, images) VALUES (%s, %s, %s, CONCAT('library/',%s), CONCAT('images/',%s))" , (bookname, author, year, book_link, images))
         result = "<p>Congratulations! Your book_information was inserted successfully.</p>"
         connection.commit()
    except db.Error :
          result  = """DB is in trouble at the moment. Call again later."""
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
                    answer ="""
                      <FIELDSET class = "form">
                      <LABEL>Fill the form</LABEL>
                      <p class="warn"> To see the form please submit both files.</p>
                      <p class ="warn"> If you do not see the form press REFRESH button in your browser.</p>
                       <form action = "upload.py" method = "get" id="form">
                       <p>Book name:<input type="text" name="bookname" id="book_name"></p>
                       <span class="err" id = "book_msg">%s</span><br>
                       <p>A u t h o r :<input type="text" name="author" id="author"></p>
                        <span class="err" id = "author_msg">%s</span><br>
                        <p>Y  e  a  r  :<input type="text" name="year" id="year"></p>
                        <span class="err" id = "year_msg">%s</span><br>
                         <p class = "warn"> Please type files  you submitted  with the extension.</p>
                       <p class = "warn"> For example  *.txt and  *.jpg</p>
                       <p>Name of the book file: <input type="text" name="book_link" id="book_link"> </p>
                       <p>Name of the image file:<input type="text" name="images" id="images"></p>
                     <p><input type="submit" value="Submit"></p>
                     </form>
                     </FIELDSET>
                     <FIELDSET class = "form">
                      <LABEL>Choose txt file</LABEL>
                     <form enctype="multipart/form-data" action="save_file.py" method="post" id="form_txt">
                     <p>File: <input type="file" name="file1" id="file1_txt"></p>
                     <p><input type="submit" value="Upload" id="file_txt"></p>
                     <span class="err" id = "file_txt_msg">%s</span><br>
                     <p class = "warn"> Please use txt-format for books.</p>
                    </form>
                    </FIELDSET>
                    <FIELDSET class="form">
                    <LABEL>Choose image file</LABEL>
                    <form enctype="multipart/form-data" action="save_image.py" method="post" id="form_img">
                    <p>File: <input type="file" name="file2" id="file2_img"></p>
                    <p><input type="submit" value="Upload" id="file_img"></p>
                    <span class="err" id = "file_img_msg">%s</span><br>
                    <p class = "warn"> Please use jpg-format for pictures.</p>
                    </FIELDSET>"""% (book_msg, author_msg, year_msg, file_txt_msg, file_img_msg)
                else:
                    answer= '<p class = "warn"> You need to be logged in to upload</p><a href = login.py>Click here to log in.</a>'
            else:
                answer= '<p class = "warn"> You need to be logged in to upload</p><a href = login.py>Click here to log in.</a>'
        else:
            answer= '<p class = "warn"> You need to be logged in to upload</p><a href = login.py>Click here to log in.</a>'
    else:
        answer= '<p class = "warn"> You need to be logged in to upload</p><a href = login.py>Click here to log in.</a>'
             
except IOError:
    result ='<p> We are experiencing problems at the moment. Please call back later.</p>'
                
   
print("""<!DOCTYPE HTML>
        <html lang="en">
           <head>
             <TITLE> Upload Form </TITLE>
             <LINK rel = "stylesheet" href = "library.css">
             <SCRIPT src="form.js">
             </SCRIPT>
          </head>
          <body>
            <H2>Form for Uploading Books</H2>
            %s
            <br>
            <p>%s</p>
            <span class = "err" id="refresh_msg"></span>
            <A HREF = 'index.py'><--- Press to Reurn</A><br>
          </body>
        </html>""" %(answer, result))
 
