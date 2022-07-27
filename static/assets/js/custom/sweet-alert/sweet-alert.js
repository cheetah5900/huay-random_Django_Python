
  function ExecuteTimerAlert() {
    let timerInterval;
    Swal.fire({
      title: "กำลังโหลดข้อมูล!",
      html: "ถ้าเกิน 30 วินาที แล้วยังค้นหาไม่เสร็จ ให้ Refresh หน้าแล้วค้นหาใหม่ ตอนนี้เหลืออีก <b></b> วินาที",
      timer: 30000,
      didOpen: () => {
        Swal.showLoading();
        const b = Swal.getHtmlContainer().querySelector("b");
        timerInterval = setInterval(() => {
          b.textContent = (Swal.getTimerLeft() / 1000).toFixed(0);
        }, 1000);
      },
    }).then((result) => {
      /* Read more about handling dismissals below */
      if (result.dismiss === Swal.DismissReason.timer) {
        Swal.fire("ค้นหาไม่สำเร็จ", "กรุณา Refresh และลองใหม่", "error");
      }
    });
  }