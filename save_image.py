#!/usr/local/bin/python3
import cgi, os
import cgitb; cgitb.enable()

print ('Content-Type: text/html')
print()

try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

form = cgi.FieldStorage()

# A nested FieldStorage instance holds the file
fileitem = form['file2']

# Test if the file was uploaded
if fileitem.filename:
   
   # strip leading path from file name to avoid directory traversal attacks
   fn = os.path.basename(fileitem.filename)
   open('images/' + fn, 'wb').write(fileitem.file.read())
   message = 'The file "' + fn + '" was uploaded successfully'
else:
   message = 'No file was uploaded'
   
print ("""<!DOCTYPE HTML>
       <html lang = "en">
       <HEAD>
       <TITLE>Uploading</TITLE>
         <script>
          function goBack(){
          window.history.back();
          }
         </script>
       </HEAD>
       <body>
       <p>%s</p>
       
        </body>
       </html>
""" % (message))
