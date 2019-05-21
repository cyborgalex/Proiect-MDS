$(document).ready(function() {
    $('.mobile-toggle').click(function() {
        
        if ($('.main_h').hasClass('open-nav')) {
            $('.main_h').removeClass('open-nav');
        } else {
            $('.main_h').addClass('open-nav');
        }
    });
    
    
    $('.main_h li a').click(function() {
        if ($('.main_h').hasClass('open-nav')) {
            $('.navigation').removeClass('open-nav');
            $('.main_h').removeClass('open-nav');
        }
    });
    
    
    $('nav a').click(function(event) {
        var id = $(this).attr("href");
        var offset = 70;
        var target = $(id).offset().top - offset;
        $('html, body').animate({
            scrollTop: target
        }, 500);
        event.preventDefault();
    });




    
    showSlides(slideIndex);

});


var slideIndex = 1;
function plusSlides(n) {
    showSlides(slideIndex += n);
  }
  
  function currentSlide(n) {
    showSlides(slideIndex = n);
  }
  
  function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    if (n > slides.length) {slideIndex = 1}    
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";  
    dots[slideIndex-1].className += " active";
  }



function like(id,action){
    $('.bone').toggleClass('red');
    $.ajax({
        url: "/bone",
        type: "post",
        datatype: "JSON",
        contentType: "application/json",
        data: JSON.stringify({
            id:id,
            action:action
        })
    });
}




//comentarii




function $(element) {
	return document.getElementById(element);
}
const alertBox = $('alert');
let commentSubmit = $('btn_add_comment');
const commentBox  = $('text_comment');
let commentList   = $('list_comments');

commentSubmit.addEventListener('click', function(e) {
	e.preventDefault();
  const d = new Date();
  let time = d.toLocaleTimeString();
	let comment  = commentBox.value.trim();
	let newLI = document.createElement('li');
  
  if (commentBox.value.length > 1) {
  $('alert').innerText = '';
  comment = `<p class="comment">${comment}</p><p class="date"><b>Posted on: ${time}</b></p>`;
	newLI.innerHTML = comment;
	commentList.appendChild(newLI);

  fadeOut(newLI);
    
    commentBox.value = '';
  } else {
    $('alert').innerText = 'Please enter a comment!';
  }
}, false);


function fadeOut(element) {
    element.style.background = "pink";
    var opacity = 1,
    fps = 90;  
    function decrease () {
        opacity -= 0.05;
        if (opacity <= .40){
            // complete
            element.style.background = "white";
            element.style.opacity = 1;
            return true;
        }
        element.style.opacity = opacity;
        setTimeout(decrease,fps);
    }
    decrease();
}






