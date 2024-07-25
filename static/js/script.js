

// owl carousel

$(document).ready(function(){
    $('#phone-carousel').owlCarousel({
        loop:true,
        margin:10,
        nav:false,
        dots:true,
        autoplay:true,
        autoplayTimeout:2000,
        autoplayHoverPause:true,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:3
            },
            1000:{
                items:5
            }
        }
    });
});

// static carousel
// headphone-carousel

$(document).ready(function(){
    $('#headphone-carousel').owlCarousel({
        loop:true,
        margin:10,
        nav:true,
        dots:true,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:3
            },
            1000:{
                items:5
            }
        }
    });
});



// pure js
// const pluscart = document.querySelector('.plus-cart');
// pluscart.addEventListener('click', function(){
//     console.log("plus button clicked")
//     const id = pluscart.getAttribute('pid');
//     console.log(id);
// })

