

// ลบรายการ
function deleteUser(id) {
  // คำสั่ง confirm
  var action = confirm("แน่ใจหรือไม่ว่าต้องการลบ ?");
  // ดึงค่า absolute url จากตัวแปร
  var urls =  $("#url_crud_ajax_delete").attr("data-url");
  // ถ้าการ confirm เป็นยืนยันค่อยจะเริ่มลบ
  if (action != false) {
    $.ajax({
      // url ที่จะส่งไป
        url: urls,
        // ข้อมูลที่จะส่งไปไฟล์ view.py
        data: {
            'id': id,
        },
        // ประเภทข้อมูล
        dataType: 'json',
        // เมื่อสำเร็จจะส่ง data กลับมา
        success: function (data) {
          // เช็คดูว่ามี key deleted มัย ถ้าเป็นจริงจะเข้าเงื่อนไ
            if (data.deleted) {
              // ถ้ามีก็สั่งลบแถวนั้นไป
              $("#userTable #user-" + id).remove();
            }
        }
    });
  }
}