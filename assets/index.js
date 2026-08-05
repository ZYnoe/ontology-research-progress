(function () {
  "use strict";

  var form = document.getElementById("date-jump");
  var input = document.getElementById("date-input");
  var message = document.getElementById("jump-message");

  function showMessage(text) {
    message.textContent = text;
    message.classList.remove("hidden");
  }

  // 默认选中今天（本地时区）
  var now = new Date();
  var local = new Date(now.getTime() - now.getTimezoneOffset() * 60000);
  input.value = local.toISOString().slice(0, 10);

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var date = input.value;
    if (!date) {
      return;
    }
    var url = "entries/" + date + ".html";

    fetch(url, { method: "HEAD" })
      .then(function (res) {
        if (res.ok) {
          window.location.href = url;
        } else {
          showMessage("这一天还没有记录：" + date);
        }
      })
      .catch(function () {
        // 本地以 file:// 打开时 fetch 可能不可用，直接跳转
        window.location.href = url;
      });
  });
})();
