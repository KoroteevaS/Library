#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage, escape
from hashlib import sha256
from time import time
import pymysql as db
from hashlib import sha256
from time import time
import shelve
#from shelve import open
from os import environ
from http.cookies import SimpleCookie

print('Content-Type: text/html')
print()

comments = ''
form_data= FieldStorage()
result = ''
form = ''
bookname1 = ''
bookname = ''
author1 = ''
year1 = 0
year2 = 2100
lst = ''
logreg ="""<button onclick="window.location.href='login.py'">Login</button>
            <button onclick="window.location.href='register.py'">Register</button>"""
logreg1 = ''
name = ''
exclam = ''
linecount = 0
end = 100
lst2 = []

try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if  http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in http_cookie_header:
            sid = cookie['sid'].value
            session_store = shelve.open('sess_' + sid, writeback=True)
            if 'authenticated' in session_store:
                if session_store['authenticated'] == True:
                    name = session_store['username']
                    try:
                        connection = db.connect('cs1dev.ucc.ie', 'sy1',  'gaequaez', 'csdipact2015_1_sy1')
                        cursor = connection.cursor(db.cursors.DictCursor)
                        cursor.execute('SELECT username FROM users WHERE username = %s', (name))
                        row = cursor.fetchone()
                        logreg = "Hello, "
                        logreg1 = """<button onclick="window.location.href='logout.py'">Logout</button>"""
                        exclam = '!'
                    except db.Error:
                        comments = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
except IOError:
    result ='<p> We are experiencing problems at the moment. Please call back later.</p>'

try:
    connection = db.connect('cs1dev.ucc.ie', 'sy1',  'gaequaez', 'csdipact2015_1_sy1')
    cursor = connection.cursor(db.cursors.DictCursor)
    cursor.execute('SELECT book_link, images FROM library ORDER BY book_id DESC LIMIT 7')
    lst += '<ul>'
    for row in cursor.fetchall():
        lst += """<li><a href = '%s'><img src='%s' class = "show"  alt = "book cover"></a></li>""" % (row['book_link'], row['images'])
    lst +='</ul>'
    cursor.close()
    connection.close()
        
except db.Error:
    form = '<Sorry.We are experiencing problems with getting information at the moment. Please call back later>'


if len(form_data) != 0:
    try:
        bookname = escape(form_data.getfirst('bookname', '').strip())
        author1 = escape(form_data.getfirst('author1', '').strip())
        link = escape(form_data.getfirst('images', '').strip())
        connection = db.connect('cs1dev.ucc.ie', 'sy1',  'gaequaez', 'csdipact2015_1_sy1')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute('SELECT * FROM library WHERE book_name LIKE "%'+bookname+'%" AND author LIKE "%'+author1+'%"')
        for row in cursor.fetchall():
            result += "<P>%s, %s, %s, <a href = '%s'><img src='%s' width = '50' ></a>" % (row['book_name'], row['author'],row['written'], row['book_link'], row['images'])
        cursor.close()
        connection.close()
        
    except db.Error:
        form = '<Sorry.We are experiencing problems with getting information at the moment. Please call back later>'

form +="""<input type="hidden" name="form1" value="login">
              <FORM action = "index.py" method = "get"><LABEL for= "bookname">Search by Book:</LABEL>
              <INPUT TYPE="text" name="bookname" value='%s' size = "30" maxlength = "30" id = "bookname"><br>
              <LABEL for= "author1">Search by Author:</LABEL>
              <INPUT TYPE="text" name="author1" value='%s' size = "30" maxlength = "30" id = "author1"><br>"""% (bookname, author1)
form += """<INPUT TYPE = "submit" value ="search">
              </FORM>"""




print("""<!DOCTYPE html>
    <HTML lang = "en">
       <HEAD>
         <TITLE>Library</TITLE>
        <script src="library.js"></script>
          <LINK rel = "stylesheet" href = "library.css">
      </HEAD>
      <BODY>
        <HEADER>
        <TABLE class = "hdr">
         <TR>
           <TD>
           <ul id = "slideshow">
           <li><img src="images/book.jpg" id="book" width = '200' height = '130' alt="bookart"  onmouseover="this.src='images/book_2.jpg'" onmouseout="this.src='images/book.jpg'" />
           <li><img src="images/book_2.jpg" width = '200' height = '130' alt="bookart" /></li>
           <li><img src="images/book_3.jpg" width = '200' height = '130' alt="bookart" /></li>
           <li><img src="images/book_4.jpg" width = '200' height = '130' alt="bookart" /></li>
           <li><img src="images/book_5.jpg" width = '200' height = '130' alt="bookart" /></li>
           <li><img src="images/book_6.jpg" width = '200' height = '130' alt="bookart" /></li>
           <li><img src="images/book_7.jpg" width = '200' height = '130' alt="bookart" /></li>
           <li><img src="images/book_8.jpg" width = '200' height = '130' alt="bookart" /></li>
           </ul>
           <p class = "button"><input id="bttn" value="Book Art Gallery Demonstration" type="button">
          </TD>
          <TD><H1 id = "header">Library</H1></TD>
          <TD class = "lft">
             %s
             %s
             %s
             %s
          </TD>
        </TR>
        </TABLE>
        </HEADER>
    <MAIN>
        <TABLE>
         <TR>
            <TD class = "bord">
              <a href="index.py" class="big"> MAIN</a>
            </TD>
            <TD>
            </TD>    
            <TD class = "bord">
               <a href="show_library.py" class="big">All BOOKS</a>
            </TD>
            <TD>
            </TD>
            <TD class = "bord">
                <a href="comments.py" class="big">COMMENTS</a>
            </TD>
        </TABLE>
        <TABLE class ="mn">
         <TR>
         <TD class = "tdfld">
         
        <FIELDSET class = "search" >
             %s
        </FIELDSET>
        <BR>
        <FIELDSET class = "search" >
           <form action="upload.py" method="get">
           <input type="submit" value="Upload">
         </form>
        </FIELDSET>
         </TD>
         <TD>
            <div class="text">
                 %s
           </div>
          </TD>
        </TR>
      </TABLE>
     </MAIN>
     <ASIDE>
         <h2>WHAT's NEW</h2>
           %s
    </ASIDE>
<BR>
<BR>
    <FOOTER>
    &copy; File Uploading Program from <a href = 'http://webpython.codepoint.net/cgi_file_upload'>WEB PYTHON</a>
    &copy; Images from <a href ='https://www.google.ie/search?client=ubuntu&channel=fs&q=bookart&ie=utf-8&oe=utf-8&gws_rd=cr&ei=VVYYVfbsJImP7AbC9YCoAw'>Internet</a>
    </FOOTER>
   </BODY>
 </html>""" % (logreg, name, exclam, logreg1, form, result,  lst))

