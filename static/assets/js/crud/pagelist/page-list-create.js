$("form#addPagelist").submit(function () {
// get data
var pageName = $(`input[name="page_name"]`).val().trim();
var title = $(`input[name="title"]`).val().trim();
var urls = $(`#url_page_list_create`).attr('data-url');
if(pageName){
$.ajax({
    url: urls,
    data:{
        page_name: pageName,
        title: title,
    },
    dataType: 'json',
    success: function (context) {
        if(context.newPageObject){
            appendToPageListTable(context.newPageObject);
        }
    },
});

} else {
    alert("PAGE LIST CREATE.");
}
$("form#addPagelist").trigger("reset");
return false;
});

// ฟังก์ชั่นเพิ่มแถวในตาราง
function appendToPageListTable(newPageObject) {
    // เพิ่มแถวเข้าไปในตารางที่ระบุ
    // ใน object user จะส่ง key เข้ามาหลายอันทั้ง id full_keyword address เป็นต้น 
    $("#pagelistTable > tbody:last-child").append(`
              <tr id="user-${newPageObject.id}">
              <td class="pageName" name="name">${newPageObject.page_name}</td>
              <td class="title" name="title">${newPageObject.title}</td>
                  '<td align="center">
                      <button class="btn btn-green" onClick="editUser(${newPageObject.id})" data-toggle="modal" data-target="#myModal")">แก้ไข</button>
                  </td>
                  <td align="center">
                      <button class="btn btn-red" onClick="deleteUser(${newPageObject.id})">ลบ</button>
                  </td>
              </tr>
          `);
  }
  