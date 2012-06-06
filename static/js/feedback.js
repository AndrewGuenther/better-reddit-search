function feedback(event) {
   $.ajax("/feedback", {data: {dir: event.data.dir, who: event.data.who, id: $('.searchid').attr('searchid')}})

   if (event.data.dir == 1)
      $(this).css("color", "green")
   else
      $(this).css("color", "red")

   $(this).unbind('click')
   $(this).siblings().unbind('click')
   $(this).removeClass('a b up down')
   $(this).siblings().removeClass('a b up down')
}

$('.a.up').click({dir: 1, who: 0}, feedback)
$('.a.down').click({dir: 0, who: 0}, feedback)
$('.b.up').click({dir: 1, who: 1}, feedback)
$('.b.down').click({dir: 0, who: 1}, feedback)
