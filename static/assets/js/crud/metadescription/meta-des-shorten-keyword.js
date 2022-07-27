
$("form#shortenUniqueKwMetaDes").submit(function () {
    var addMode = $('input[name="add_mode_meta_des"]').val().trim();
    var comeFrom = $('input[name="come_from_meta_des"]').val().trim();
    var pageId = $('input[name="page_id_meta_des_shorten_kw"]').val().trim();

    var urls = $('#url_meta_des_shorten_kw').attr('data-url');

    if(addMode){
        $.ajax({
            url : urls,
            data :{
                'add_mode' : addMode,
                'come_from' : comeFrom,
                'page_id' : pageId
            },
            dataType : 'json', 
            success: function(context){
                updateUniqueKwMetaDes(context);
                Swal.fire("ใช้ชุดคำนี้แล้ว", "", "success");
            }
        })
        return false;
    }else{
        alert('Please enter a mode to add to the database');
    }
});

function updateUniqueKwMetaDes(context){
    $('#amount_shorten_kw_meta_des').text("("+context.lengthShortKeyword+")");
    $('#shorten_kw_meta_des').text(context.joinShortenKeyword);
}