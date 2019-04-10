


document.write('<div class="row">');
    document.write('<a class="logo" href="#">K9</a>')
    document.write('<div class="mobile-toggle"><span></span><span></span><span></span></div>');
    document.write('<nav> <ul>');
        document.write('<li>Find a dog</li>');
        document.write('<li>About us</li>');
        document.write('<li>Log In/Sign Up</li>');
    document.write('</ul></nav>');
document.write('</div>');

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



$('.message a').click(function(){
    $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
 });

});




