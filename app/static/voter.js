$('.upvote').click(function(ev){
    var id = $(ev.currentTarget).attr('data-id');
    window.location.href = "/bbs/upvote/" + id
    //$.get( "/bbs/upvote/" + id, function( data ) {
    // change your button here, and remove its upvote_button class
    // alert(data);
    //});
});

