function deleteMetaDes(id,pid){
    console.log("Meta Description Delete")
    var action = confirm('ต้องการลบใช่หรือไม่');
    var urls = $('#url_meta_des_delete').attr("data-url");
    if(action != false){
        $.ajax({
            url : urls,
            data : {
                'md_id' : id,
                'page_id' : pid
            },
            dataType : 'json',
            success: function(context){
                if(context.deleted){
                    $("#metaDesTable #meta-"+id).remove();
                }
                Swal.fire("ลบสำเร็จแล้ว", "", "success");
            }
        })
    }
}