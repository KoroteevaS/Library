( function () {

var book_name;
var author;
var year;
var year_input;
var form, form_txt, form_img;
var file_txt, file_img;

document.addEventListener("DOMContentLoaded", init, false)

function init() 
{
     book_name      = document.querySelector('#book_name');
     book_span      = document.querySelector('#book_msg')
     author         = document.querySelector('#author');
     author_span    = document.querySelector('#author_msg');
     year           = document.querySelector('#year');
     year_span      = document.querySelector('#year_msg');
     form           = document.querySelector('#form');
     file_txt       = document.querySelector('#file_txt');
     file1_txt      = document.querySelector('#file1_txt'); 
     form_txt       = document.querySelector('#form_txt'); 
     file_img       = document.querySelector('#file_img');
     form_img       = document.querySelector('#form_img');  

     form.addEventListener('submit', validate_input, false);
     form_txt.addEventListener('submit', validate_input, false);
     form_img.addEventListener('submit', validate_input, false);
     form.style.display = 'none';
     
     //window.alert(file_txt_msg);
     book_link.value   = document.getElementById('file1_txt').value;
     images.value  = document.getElementById('file2_img').value;


     if (book_link.value !== '' && images.value !== '')
       form.style.display = 'inline';
     
}


function check_for_int(text, maximum)//for checking year
{
       var trimmed_text = text.trim();
       if (trimmed_text === "") 
        {	
          return "Mandatory field";
       }
       var number = ~~Number(trimmed_text);
       if (String(number) !== trimmed_text)
       {
 	  return "Must be a whole number";
       } 
       if( number > maximum )
       {
          return "Must be no greater then" + maximum;
       }
       return '';
}
     
function check_text(text)  //for checking text
{       
       var trimmed_text = text.trim();
       if ( trimmed_text === "" )
       {
          return "Mandatory field";
       }

       return '';
}
       
  
function validate_input(event) 
{
      book_msg   = check_text(book_name.value);
      author_msg = check_text(author.value);
      file_txt_msg  = check_text(file_txt.value);
      file_img_msg  = check_text(file_img.value);
      year_msg   = check_for_int(year.value, 2015);
      book_span.innerHTML   = book_msg;
      author_span.innerHTML = author_msg;
      year_span.innerHTML   = year_msg;
      file_txt_span.innerHTML = file_txt_msg;
      file_img_span.innerHTML = file_img_msg;
      if (year_msg || book_msg || author_msg || file_txt_msg || file_img_msg)
      {
	 event.preventDefault();
      }   
}
 }) ();
