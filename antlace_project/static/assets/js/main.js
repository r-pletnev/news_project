$('.menu-trigger').on('click', function(event){
  $(this).toggleClass('active');
  if($(this).hasClass('active')) {
    $('.menu ul').slideDown(200);
  } else {
    $('.menu ul').slideUp(200);
  }
});
