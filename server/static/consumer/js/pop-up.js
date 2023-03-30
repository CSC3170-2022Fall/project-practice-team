$('.show-modal').on('click', function(){
    var $img = $(this).parents('div').eq(1).children('figure').eq(0).children('img').eq(0);
    let img_sell_url = $img.attr('src');

    let price = $img.attr('price');
  
    $('.pop-up').css('display', 'initial');
    $('.modal-background').css('display', 'block');
    $('.overlay').css('display', 'block');
  
  
    $('.pop-up .pop-up-left .image-holder').append(
      $("<img>", {
        src : img_sell_url,
        id : $(this).attr('id')
      }).css({
        "border": "white 3px solid",
        "max-width": "100%",
        "max-height": "100%"
      })
    );
    $('#price').empty().append('Price: ' + price + '$');
  
  });
  
  
  // Close Modal
  
  
  $('.pop-up-close').on('click', function(){
    $('.pop-up').css('display', 'none');
    $('.modal-background').css('display', 'none');
    $('.pop-up .pop-up-left .image-holder img').remove();
    $('.wish-list-gallery .wish-list-item').remove();
    $('.overlay').css('display', 'none');
  });
  