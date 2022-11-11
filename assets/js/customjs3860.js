// page animation main
! function(e) {   
    (new WOW).init();    
}(jQuery);
// page animation main end

$(document).ready(function(){
     $("#sideNav").click(function(){
        if($(this).hasClass('toggle')){
            $(".menu").addClass("add-mob-menu");            
            $(this).removeClass('toggle');
            $("#sideNav i").addClass("fa-times");
            $("#sideNav i").removeClass('fa-bars');
        } else{
            $(".menu").removeClass("add-mob-menu");
            $(this).addClass('toggle');
            $("#sideNav i").removeClass("fa-times");
            $("#sideNav i").addClass('fa-bars');
        }                   
     })
 });

$(document).ready(function(){
     $(".footerplus").click(function(){
        if($(this).hasClass('f-toggle')){
            $(".m-footer").slideToggle();            
            $(this).removeClass('f-toggle');
            $(".footerplus i").addClass("fa-minus");
            $(".footerplus i").removeClass('fa-plus');
        } else{
            $(".m-footer").slideToggle("add-mob-menu");
            $(this).addClass('f-toggle');
            $(".footerplus i").removeClass("fa-minus");
            $(".footerplus i").addClass('fa-plus');
        }                   
     })
 });


$(document).ready(function(){
    $(window).width()<560 
    {
        $(".dpd-menu a").click(function(){
        $(".dropdown-content").slideToggle(); 
        }) 
    }
});

// login popup
var modal = document.getElementById('message');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
// signup popup
var modal = document.getElementById('call');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}



 //marq slider on index page
 $(document).ready(function () {
    $('.service-slide').slick({
        dots: false,
        infinite: true,
        speed: 1000,
        slidesToShow: 5,
        slidesToScroll: 1,
        autoplay: true,
        responsive: [{
                breakpoint: 1024,
                settings: {
                    slidesToShow: 5,
                    slidesToScroll: 1,
                    // centerMode: true,
                }
            }, {
                breakpoint: 800,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                }
            }, {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2,
                    infinite: true,
                }
            }, {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true,
                    autoplay: false,
                    autoplaySpeed: 2000,
                }
            }]
        });
    });

 $(document).ready(function () {
    $('.price-plan-slide').slick({
        dots: false,
        infinite: true,
        speed: 1000,
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        responsive: [{
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    // centerMode: true,
                }
            }, {
                breakpoint: 800,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                }
            }, {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2,
                    infinite: true,
                }
            }, {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true,
                    autoplay: false,
                    autoplaySpeed: 2000,
                }
            }]
        });
    });

 $(document).ready(function () {
    $('.testimonial-slide').slick({
        dots: false,
        infinite: true,
        speed: 1000,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        responsive: [{
                breakpoint: 1024,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    // centerMode: true,
                }
            }, {
                breakpoint: 800,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true,
                }
            }, {
                breakpoint: 600,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true,
                }
            }, {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true,
                    autoplay: false,
                    autoplaySpeed: 2000,
                }
            }]
        });
    });



/*for header animate on top Scroll--*/    
    $(document).ready(function() {
        $(window).scroll(function() {
            if ($(this).width()>560)
            {
                if ($(window).scrollTop() > 50) {
                   $(".head").addClass("stricky-fixed stricked-head"); 
                }
                else
                {
                   $(".head").removeClass("stricky-fixed stricked-head"); 
                }
            }
            else
            {
              $(".head").addClass("stricky-fixed stricked-head"); 
            }
        });
    });

/*for top Scroll--*/
$(document).ready(function() {
    $(window).scroll(function() {
        if ($(this).scrollTop()>150)
         {
            $('#top-scroll').fadeIn();
         }
        else
         {
          $('#top-scroll').fadeOut();
         }
    })
});  
$(document).ready(function() {
    $('#top-scroll').click(function() {
        $('html,body').animate({scrollTop: $('.top-scroll').offset().top});
    })    
});
     
/*for top Scroll end--*/

/*service radio*/
$(document).ready(function(){
    $('input[type="radio"]').click(function(){
        var inputValue = $(this).attr("value");
        var targetBox = $("." + inputValue);
        $(".box").not(targetBox).hide();
        $(targetBox).show();
    });
});

/* select2 form*/
// $(document).ready(function() {
//    $(".form-control2").select2();
// });


/*-------accordion plus minus-------*/
$(document).ready(function(){
    $(".collapse.show").each(function(){
        $(this).prev(".card-header").find(".fa").addClass("fa-minus").removeClass("fa-plus");
    });
    $(".collapse").on('show.bs.collapse', function(){
        $(this).prev(".card-header").find(".fa").removeClass("fa-plus").addClass("fa-minus");
    }).on('hide.bs.collapse', function(){
        $(this).prev(".card-header").find(".fa").removeClass("fa-minus").addClass("fa-plus");
    });
});


/*-------comments click on answer-------*/
$(document).ready(function(){
    $("#comment").click(function(){
        $(".comment-form").slideToggle();
    });
    $("#popup-comment").click(function(){
        $(".comment-form").slideToggle();
    });
});
/*-------comments click on answer end-------*/

$(document).ready(function(){
     $(".add-to-cart a").click(function(){
        if($(this).hasClass('cart-btn')){
            $(".btn-checkout").addClass("show-btn-checkout");            
            // $(this).removeClass('cart-btn');
            // $(".add-to-cart i").addClass("fa-times");
            // $(".add-to-cart i").removeClass('fa-bars');
        } else{
            $(".btn-checkout").removeClass("show-btn-checkout");
            // $(this).addClass('toggle');
            // $(".add-to-cart i").removeClass("fa-times");
            // $(".add-to-cart i").addClass('fa-bars');
        }                   
     })
 });

/*---remove selected service on checkout page---*/
$(document).ready(function(){
    $(document).on("click", ".delete", function(){
        $(this).parents("tr").remove();
    });
});


/*---read mor on about us page---*/
    $(document).ready(function() {
        var showChar = 130;  // How many characters are shown by default
        var ellipsestext = "...";
        var moretext = "Read more...";
        var lesstext = "Show less";
        

        $('.more').each(function() {
            var content = $(this).html();
     
            if(content.length > showChar) {
     
                var c = content.substr(0, showChar);
                var h = content.substr(showChar, content.length - showChar);
     
                var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';     
                $(this).html(html);
            }     
        });
     
        $(".morelink").click(function(){
            if($(this).hasClass("less")) {
                $(this).removeClass("less");
                $(this).html(moretext);
            } else {
                $(this).addClass("less");
                $(this).html(lesstext);
            }
            $(this).parent().prev().toggle();
            $(this).prev().toggle();
            return false;
        });
    });
 
//form vcalue insert on online payment
$('#checkOutForm').validate({ 
    rules: {
      name: "required",
      vehicle_no:"required",
      mobile:"required",
      //country:"required",
      //state:"required",
      //city:"required",
      email:"required",
    },
    messages: {
      name: "Please Enter Full Name",
      vehicle_no:"Vechile Number Required",
      mobile:"Contact Number Required",
      //country: 'Please select country',
      //state:"Please select state",
      //city:"Please select city",
      email:"Please enter email id",
    },
    submitHandler: function(form) {
      form.submit();
      
    }
    });
$('#contact-form').validate({ 
    rules: {
      name: {
        required: true,
        minlength: 2,
      },
      contact_no: {
        required: true,
        number: true,
        minlength: 10,
        maxlength: 10,
        RegExp:/^(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}$/
      },
     
      email: {
        required: true,
        email: true
      }},
    messages: {
      name: "Please Enter Full Name",
      contact_no:"Please Enter Valid 10 Digit Mobile Number",
      email:"Please enter valid email id",
    },
    submitHandler: function(form) {
      form.submit();
      
    }
    });

    /*-------mobile search hide/show-------*/
//  $(document).ready(function() {
//     if ($(window).width() < 640) {
     
//         $(".search-btn").click(function(){
//             $(".filter-section").addClass("show-filter-section");            
//             $(".btn-edit").addClass("show-btn-edit");
//             $("#brand_new_search1").css("border-color", "red");

//         })
//     }
  
//     if ($(window).width() < 640) {
//         $(".btn-edit").click(function(){
//             $(".btn-edit").removeClass("show-btn-edit");
//             $(".filter-section").removeClass("show-filter-section");
//         })
//     }
   
// });
/*-------mobile search hide/show end-------*/