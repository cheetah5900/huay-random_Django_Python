$("form#updateMetaDes").submit(function () {
  console.log("Meta Description Update");
  var keywordId = $('input[name="keyword_id"]').val().trim();
  var fullKeyword = $('input[name="full_keyword_meta_des_edit"]').val().trim();
  var shortKeyword = $('input[name="shorten_keyword_meta_des_edit"]').val().trim();
  var pageId = $('input[name="page_id_meta_des_edit"]').val().trim();
  var urls = $("#url_ajax_meta_des_update").attr("data-url");
  if (keywordId) {
    $.ajax({
      url: urls,
      data: {
        keyword_id: keywordId,
        full_keyword: fullKeyword,
        shorten_keyword: shortKeyword,
        page_id: pageId,
      },
      dataType: "json",
      success: function (context) {
        updateToMataDesTable(context.updateMetaDesList);
        Swal.fire("แก้ไขสำเร็จแล้ว", "", "success");
      },
    });
  } else {
    alert("Meta Description Edit Error");
  }
  $("form#updateMetaDes").trigger("reset");
  $("#editData").hide();
  return false;
});
function updateToMataDesTable(updateMetaDesList) {
  $("#metaDesTable #meta-" + updateMetaDesList.id)
    .children(".metaDesData")
    .each(function () {
      var attr = $(this).attr("name");
    //   console.log("attr : " + attr);
      if (attr == "full_keyword") {
        $(this).text(updateMetaDesList.full_keyword);
      } else if (attr == "amount_this_page_fk") {
        $(this).text(updateMetaDesList.amount_this_page_fk);
      } else if (attr == "amount_all_page_fk") {
        $(this).text(updateMetaDesList.amount_all_page_fk);
      } else if (attr == "shorten_keyword") {
        $(this).text(updateMetaDesList.shorten_keyword);
      } else if (attr == "amount_this_page_sk") {
        $(this).text(updateMetaDesList.amount_this_page_sk);
      } else if (attr == "amount_all_page_sk") {
        $(this).text(updateMetaDesList.amount_all_page_sk);
      }
    });
}
