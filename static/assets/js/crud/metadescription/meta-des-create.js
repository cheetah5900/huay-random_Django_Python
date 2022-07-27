$("form#addMetaDescription").submit(function () {
    console.log("Meta Description Create");
    var fullKeyword = $(`input[name="full_keyword_meta_des_create"]`).val().trim();
    var pageId = $(`input[name="page_id_meta_des_create"]`).val().trim();
    var urls = $(`#url_meta_des_create`).attr('data-url')
    if(fullKeyword){
        $.ajax({
            url:urls,
            data: {
                full_keyword:fullKeyword,
                page_id:pageId
            },
            dataType: 'json',
            success: function (context) {
                appendToMetaDesTable(context.newMetaDesList);
                Swal.fire("เพิ่มสำเร็จแล้ว", "", "success");
            },
            error: function(){
                Swal.fire("มี Keyword นี้แล้ว", "กรุณาเลือก Keyword อื่น", "error");
            }
        })
    } else {
        alert("META DES KEYWORD");
    }
    $("form#addMetaDescription").trigger("reset");
    return false;
});
function appendToMetaDesTable(newMetaDesList) {
    $('#metaDesTable > tbody:last-child').append(`
    <tr id="meta-${newMetaDesList.id}">
    <td>${newMetaDesList.counter}</td>
    <td class="fullKeyword metaDesData" name="full_keyword">${newMetaDesList.full_keyword}</td>
    <td class="text-center metaDesData" name="amount_this_page_fk">${newMetaDesList.amount_this_page_fk}</td>
    <td class="text-center metaDesData" name="amount_this_page_fk">${newMetaDesList.amount_this_page_fk}</td>
    <td class="shortKeyword metaDesData" name="shorten_keyword">${newMetaDesList.shorten_keyword}</td>
    <td class="text-center metaDesData" name="amount_this_page_sk">${newMetaDesList.amount_this_page_sk}</td>
    <td class="text-center metaDesData" name="amount_all_page_sk">${newMetaDesList.amount_all_page_sk}</td>
        '<td align="center">
            <button class="btn btn-green" onClick="editMetaDes(${newMetaDesList.id})" data-bs-toggle="modal" data-bs-target="#editData")">แก้ไข</button>
            <button class="btn btn-red" onClick="deleteMetaDes(${newMetaDesList.id},${newMetaDesList.page_id})">ลบ</button>
        </td>
    </tr>
    `)
}