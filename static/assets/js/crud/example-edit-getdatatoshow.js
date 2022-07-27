// แสดงข้อมูลสำหรับการแก้ไข
function editUser(id) {
  // ถ้าส่ง id เข้ามา
    if (id) {
      // user-id ให้เอามาเป็น tr_id
      tr_id = "#user-" + id;
      // class userName ของแถวนี้เอามาเก็บใส่ตัวแปร name
      name = $(tr_id).find(".userName").text();
      // ตั้งค่าให้กับ input โดยใช้ .val
      $('#form-id').val(id);
      $('#form-name').val(name);
    }
  }