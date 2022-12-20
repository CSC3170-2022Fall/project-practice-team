

$('.show-modal').on('click', function(){
    let img_sell_url = $(this).parents('div').eq(1).children('figure').eq(0).children('img').eq(0).attr('src');
  
    $('.pop-up').css('display', 'initial');
    $('.modal-background').css('display', 'block');
    $('.overlay').css('display', 'block');
  
  
    $('.pop-up .pop-up-left .image-holder').append(
      $("<img>", {
        src : img_sell_url
      }).css({
        "border": "white 3px solid",
        "max-width": "100%",
        "max-height": "100%"
      })
    );
  
  });
  
  
// Close Modal
  
  
$('.pop-up-close').on('click', function(){
  $('.pop-up').css('display', 'none');
  $('.modal-background').css('display', 'none');
  $('.pop-up .pop-up-left .image-holder img').remove();
  $('.overlay').css('display', 'none');
});
  
  
// $('.barter-tut-pop-up .pop-up-close').on('click', function(){
//   $('.barter-tut-pop-up').css('display', 'none');
//   $('.modal-background').css('display', 'none');
//   $('.overlay').css('display', 'none');
// });
  

// Image Selected Effect
$('.wish-list-gallery .wish-list-item img').on('click', function(){
  $(this).toggleClass('selected');
  var $sib = $(this).parents().eq(0).siblings().eq(0).children('img').eq(0); 
  if ($sib.hasClass('selected')){
    $sib.removeClass('selected');
    
  }
});


// $('.barter-tut').on('click', function(){
//   $('.barter-tut-pop-up').css('display', 'block');
//   $('.modal-background').css('display', 'block');
//   $('.overlay').css('display', 'block');

// });


$('.pop-up-right button').on('click', function(){
  var selected = $('.pop-up-right .selected');
  if (selected.length < 1){
    alert('You need to select one game to make the deal!');
    return;
  }
  $('.modal-confirm').css('display', 'block');
});

$('.modal-confirm .close-button').on('click', function(){
  $('.modal-confirm').css('display', 'none');
});
