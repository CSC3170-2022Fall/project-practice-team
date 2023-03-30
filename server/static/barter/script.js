

$('.show-modal').on('click', function(){
    let toSell = $(this).parents('div').eq(1).children('figure').eq(0).children('img').eq(0);
    let img_sell_url = toSell.attr('src');
    let img_id = toSell.attr('id');
    let price = toSell.attr('price');
    let date  = toSell.attr('date');
    let seller_id = toSell.attr('con-id')
  
    $('.pop-up').css('display', 'initial');
    $('.modal-background').css('display', 'block');
    $('.overlay').css('display', 'block');
  
  
    $('.pop-up .pop-up-left .image-holder').append(
      $("<img>", {
        src : img_sell_url,
        id  : img_id,
        seller_id : seller_id 
      }).css({
        "border": "white 3px solid",
        "max-width": "100%",
        "max-height": "100%"
      })
    );

    $('#price').empty().append(
      'Price: ' + price + '$'
    );
    // $('#date').empty().append(date);

    // var wish_list = $('.wish-list-display img');
    var wish_list = $(this).parents('div').eq(1).children('.wish-list-display').eq(0).find('img');

    for(let i=0; i<wish_list.length; i++){
      let item_id = wish_list.eq(i).attr('id');
      let itemHTML =  `<div class="wish-list-item mb-5">
          <img src="/static/pics/${item_id}.jpg" alt="Image" class="img-fluid" id="${item_id}">
          </div>`;
      $('.wish-list-gallery').append(itemHTML);
    }
  
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
$(document).on('click', '.wish-list-gallery .wish-list-item img', function(){
  $(this).toggleClass('selected');
  var $sib = $(this).parents().eq(0).siblings().eq(0).children('img').eq(0); 
  if ($sib.hasClass('selected')){
    $sib.removeClass('selected');
    
  }
});



$('.pop-up-right button').on('click', function(){
  var selected = $('.pop-up-right .selected');
  if (selected.length < 1){
    alert('You need to select one game to make the deal!');
    return;
  }

  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  var buyer_id = urlParams.get('con_id');

  var wish_id = selected.attr('id');
  var sell_id = $('.pop-up-left img').attr('id');
  var seller_id = $('.pop-up-left img').attr('seller_id');


  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth()+1).padStart(2, '0');
  var yyyy = today.getFullYear();

  today = mm + ' ' + dd + ' ' + yyyy;



  $.ajax({
    url : '/consumer/barter-deal',
    type: 'POST',
    dataType: 'json',
    data: jQuery.param({
      buyer_id  : buyer_id,
      seller_id : seller_id,
      sell_id : sell_id,
      wish_id : wish_id,
      date    : today
    }),
    success: function(response){
      var state = response.state;
      alert(state);
      if (state == 'successful'){
        $('#success').css('display', 'block');
      }
      else if(state == 'recursive'){
        $('#failure .prompt').empty().append('You Cannot Barter with Yourself');
        $('#failure').css('display', 'block');
      }

      else if(state == 'not_own'){
        $('#failure .prompt').empty().append('You Don\'t Own the Game');
        $('#failure').css('display', 'block');
      }
    }
  })

});

$('.modal-confirm .close-button').on('click', function(){
  $('.modal-confirm').css('display', 'none');
});
