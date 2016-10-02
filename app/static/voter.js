$('.upvote').click(function(ev){
    var id = $(ev.currentTarget).attr('data-id');
    $.get( "/bbs/upvote/" + id, function( data ) {
     data = jQuery.parseJSON(data);
     if(data.likes == -1){
         window.location.href=window.location.href
     }
     else{
         $("#"+id).text(data.likes);
         $("#"+data.author).text(data.awards);
     }
    });
});

