
// เมื่อเกิดการ Submit Form
$("form#updateUser").submit(function() {
  // รับค่าจาก input ที่มี arrtibute ชื่อ name ค่าเท่ากับ formId formName
    var idInput = $('input[name="formId"]').val().trim();
    var nameInput = $('input[name="formName"]').val().trim();
    
    // get absolute url from form in html
    // รับ absolute url อัพเดทจากฟอร์มมาด้วย
    var urls =  $("#url_crud_ajax_update").attr("data-url");
    // ถ้า nameInput ถูกเซ็ต
    if (nameInput) {
        // Create Ajax Call
        $.ajax({
          // url ที่จะ view.py
            url: urls,
            // ข้อมูลที่จะส่งไป view.py
            data: {
                'id': idInput,
                'name': nameInput,
            },
            // ประเภทข้อมูล
            dataType: 'json',
            // เมื่อสำเร็จจะส่ง data กลับมา เป็นเหมือน context
            success: function (data) {
              // เช็คว่ามี data.user มั้ย user เป็นเหมือน key ของ context มีค่าเป็น object ภายในมี id และข้อมูลอื่นๆ
                if (data.user) {
                  // ถ้ามีก็โยน object user เข้าไปในฟังก์ชั่นนี้
                  updateToUserTabel(data.user);
                }
            }
        });
       } else { // ถ้าไม่ได้รับค่า nameInput
        alert("EDIT EXAMPLE");
    }
    // reset แบบฟอร์ม
    $('form#updateUser').trigger("reset");
    // ซ่อน modal
    $('#myModal').modal('hide');
    return false;
});
// อัพเดทตารางรวมรายการ
function updateToUserTabel(user){
  // ชี้ไปที่ id userTable และ ย่อยลงมาเป็น id user-id ทีนี้เอาตัวลูกมันทุกตัวที่มีคลาสว่า userData แต่ละตัวไปทำฟังก์ชั่นต่อไปนี้ สาเหตุที่ต้องเลือกคลาส userDara แทนการบอกว่า td ทั้งหมด เพราะปุ่ม edit และปุ่ม delete 
    $("#userTable #user-" + user.id).children(".userData").each(function() {
      // ดึงค่าจาก attribute name ของแต่ละตัวมาเก็บใส่ตัวแปรชื่อ attr ของ td ออกมา
        var attr = $(this).attr("name");
        // ถ้าดึงค่าแล้ว attribute ดังกล่าวมีค่าเท่ากับ name 
        if (attr == "name") {
          // ในช่องนี้ให้ตั้งค่า text ด้วยค่า user.name
          $(this).text(user.name);
          // ถ้าดึงค่าแล้ว attribute ดังกล่าวมีค่าเท่ากับ address 
        } else if (attr == "address") {
          // ในช่องนี้ให้ตั้งค่า text ด้วยค่า user.address
          $(this).text(user.address);
        } else {
          $(this).text(user.age);
        }
      });
}