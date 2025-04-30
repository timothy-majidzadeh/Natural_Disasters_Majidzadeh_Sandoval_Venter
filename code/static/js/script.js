$(document).ready(function(){
    // Enable smooth scrolling
    $('.nav-link').click(function(e){
        e.preventDefault();
        var target = $(this).attr('href');
        $('html, body').animate({
            scrollTop: $(target).offset().top
        }, 500);

        // Collapse the menu when a link is clicked
        $('.navbar-collapse').collapse('hide');
    });

    // Enable scrollspy to update the navbar links based on scroll position
    $('body').scrollspy({ target: '#navbar-example' });

    // Collapse the menu when clicking outside of it
    $(document).click(function(event) {
        var clickover = $(event.target);
        var $navbar = $(".navbar-collapse");               
        var _opened = $navbar.hasClass("show");
        if (_opened === true && !clickover.hasClass("navbar-toggler")) {      
            $navbar.collapse('hide');
        }
    });
});
