( function () {

//this group for art gallery
var img_elements;
var num_of_images;
var current_image_index;


document.addEventListener("DOMContentLoaded", init, false);


function init() 
    {
     //art gallery
     var imgBttn;
     img_elements=document.querySelectorAll('#slideshow img');
     num_of_images = img_elements.length;
     imgBttn=document.querySelector("#bttn");
     imgBttn.addEventListener('click', goto_image, false);
     //hiding images
     for (var i = 0; i < num_of_images; i +=1 )
         {
          img_elements[i].style.display = 'none';
         }
        current_image_index =0;
        goto_image(null);
     }
  
function goto_image(event) // shows and hides the pictures and change them
    {
    img_elements[current_image_index].style.display = 'none';
    if(! event ){}
    else if(event){
      if(current_image_index < num_of_images - 1)
      {
      current_image_index+=1;
      }
      else 
      { 
       current_image_index = 0 
      }
    } 
   img_elements[current_image_index].style.display = 'inline';
    }
    
}) ();
