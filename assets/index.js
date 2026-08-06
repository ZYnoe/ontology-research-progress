(function () {
  "use strict";

  var form = document.getElementById("date-jump");
  var input = document.getElementById("date-input");
  var message = document.getElementById("jump-message");
  var countEl = document.getElementById("entry-count");
  var items = Array.prototype.slice.call(
    document.querySelectorAll(".entry-list li[data-date]")
  );
  var total = items.length;

  // Default to today (local timezone)
  var now = new Date();
  var local = new Date(now.getTime() - now.getTimezoneOffset() * 60000);
  input.value = local.toISOString().slice(0, 10);

  function showMessage(html) {
    message.innerHTML = html;
    message.classList.remove("hidden");
  }

  function clearMessage() {
    message.innerHTML = "";
    message.classList.add("hidden");
  }

  function updateHeadings() {
    var headings = document.querySelectorAll(".entry-list h3, .entry-list h4");
    headings.forEach(function (heading) {
      var visible = false;
      var next = heading.nextElementSibling;
      while (next && next.tagName !== "H3") {
        // A month (h4) only checks its own list; a year (h3) checks all
        // months below it.
        if (heading.tagName === "H4" && next.tagName === "H4") {
          break;
        }
        if (next.tagName === "UL") {
          next.querySelectorAll("li[data-date]").forEach(function (li) {
            if (li.style.display !== "none") {
              visible = true;
            }
          });
        }
        next = next.nextElementSibling;
      }
      heading.style.display = visible ? "" : "none";
    });
  }

  function applyFilter(date) {
    var visible = 0;
    items.forEach(function (li) {
      var match = li.getAttribute("data-date") === date;
      li.style.display = match ? "" : "none";
      if (match) {
        visible += 1;
      }
    });
    updateHeadings();
    if (countEl) {
      countEl.textContent =
        "Showing " + visible + " of " + total + " entries for " + date;
    }
    return visible;
  }

  function resetFilter() {
    items.forEach(function (li) {
      li.style.display = "";
    });
    document.querySelectorAll(".entry-list h3, .entry-list h4").forEach(
      function (heading) {
        heading.style.display = "";
      }
    );
    if (countEl) {
      countEl.textContent = total + (total === 1 ? " entry total" : " entries total");
    }
    clearMessage();
  }

  function showFilterMessage(visible, date) {
    var link = ' <a href="#" id="show-all">Show all</a>';
    if (visible > 0) {
      showMessage("Showing entries for " + date + "." + link);
    } else {
      showMessage("No entries for this date: " + date + "." + link);
    }
    document.getElementById("show-all").addEventListener("click", function (event) {
      event.preventDefault();
      resetFilter();
    });
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var date = input.value;
    if (!date) {
      return;
    }
    var visible = applyFilter(date);
    showFilterMessage(visible, date);
  });
})();
