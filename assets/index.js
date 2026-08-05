(function () {
  "use strict";

  var form = document.getElementById("date-jump");
  var input = document.getElementById("date-input");
  var message = document.getElementById("jump-message");

  function showMessage(text) {
    message.textContent = text;
    message.classList.remove("hidden");
  }

  // Default to today (local timezone)
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
          showMessage("No entry for this date: " + date);
        }
      })
      .catch(function () {
        // When opened via file://, fetch may be unavailable; navigate directly
        window.location.href = url;
      });
  });
})();
