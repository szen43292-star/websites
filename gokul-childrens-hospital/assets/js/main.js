/* Gokul Children's Hospital — site interactions (no dependencies) */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");

  var WA_NUMBER = "919579312398";
  var EMAIL = "deoreparikshit@gmail.com";

  /* ---------- Sticky header shadow ---------- */
  var header = document.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Desktop dropdowns: keyboard / touch support ---------- */
  document.querySelectorAll(".nav-item.has-sub > .nav-link").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      var item = btn.parentElement;
      // First tap on touch devices opens the menu instead of navigating
      if (!item.classList.contains("open") && window.matchMedia("(hover: none)").matches) {
        e.preventDefault();
        document.querySelectorAll(".nav-item.open").forEach(function (o) { o.classList.remove("open"); });
        item.classList.add("open");
      }
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".nav-item")) document.querySelectorAll(".nav-item.open").forEach(function (o) { o.classList.remove("open"); });
  });

  /* ---------- Mobile drawer ---------- */
  var drawer = document.getElementById("drawer");
  var lastFocus = null;
  function openDrawer() {
    if (!drawer) return;
    lastFocus = document.activeElement;
    drawer.classList.add("open");
    drawer.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    document.querySelectorAll("[data-open-drawer]").forEach(function (b) { b.setAttribute("aria-expanded", "true"); });
    var first = drawer.querySelector(".close-btn");
    if (first) first.focus();
  }
  function closeDrawer() {
    if (!drawer || !drawer.classList.contains("open")) return;
    drawer.classList.remove("open");
    drawer.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    document.querySelectorAll("[data-open-drawer]").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
    if (lastFocus) lastFocus.focus();
  }
  document.querySelectorAll("[data-open-drawer]").forEach(function (b) { b.addEventListener("click", openDrawer); });
  document.querySelectorAll("[data-close-drawer]").forEach(function (b) { b.addEventListener("click", closeDrawer); });
  if (drawer) {
    drawer.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", closeDrawer); });
    drawer.querySelectorAll(".m-toggle").forEach(function (t) {
      t.addEventListener("click", function () {
        var sub = document.getElementById(t.getAttribute("aria-controls"));
        var open = t.getAttribute("aria-expanded") === "true";
        t.setAttribute("aria-expanded", String(!open));
        if (sub) sub.classList.toggle("open", !open);
      });
    });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeDrawer(); });

  /* ---------- Booking dialog ---------- */
  var modal = document.getElementById("book-modal");
  document.querySelectorAll("[data-book]").forEach(function (b) {
    b.addEventListener("click", function (e) {
      if (!modal || typeof modal.showModal !== "function") return; // fall back to link href
      e.preventDefault();
      closeDrawer();
      var dept = b.getAttribute("data-book");
      var sel = modal.querySelector("select[name=department]");
      if (dept && sel) sel.value = dept;
      modal.showModal();
      var firstInput = modal.querySelector("input, select");
      // Skip auto-focus on touch screens so the keyboard doesn't cover the form
      if (firstInput && !window.matchMedia("(hover: none)").matches) setTimeout(function () { firstInput.focus(); }, 30);
    });
  });
  document.querySelectorAll("[data-close-modal]").forEach(function (b) {
    b.addEventListener("click", function () { b.closest("dialog").close(); });
  });
  if (modal) {
    modal.addEventListener("click", function (e) { if (e.target === modal) modal.close(); });
  }

  /* ---------- Appointment / enquiry forms → WhatsApp or email ---------- */
  function composeMessage(form) {
    var data = new FormData(form);
    var lines = ["Hello Gokul Children's Hospital, I would like to book an appointment."];
    var labels = {
      parent: "Parent / guardian name",
      phone: "Phone",
      email: "Email",
      child: "Child's name",
      age: "Child's age",
      department: "Department",
      visit: "Consultation type",
      date: "Preferred date",
      subject: "Subject",
      message: "Message"
    };
    Object.keys(labels).forEach(function (k) {
      var v = (data.get(k) || "").toString().trim();
      if (v) lines.push(labels[k] + ": " + v);
    });
    return lines.join("\n");
  }
  document.querySelectorAll("form[data-enquiry]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var via = (e.submitter && e.submitter.value) || "whatsapp";
      var msg = composeMessage(form);
      if (via === "email") {
        var subject = (new FormData(form).get("subject") || "Appointment request").toString();
        window.location.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(msg);
      } else {
        window.open("https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(msg), "_blank", "noopener");
      }
      var d = form.closest("dialog");
      if (d) d.close();
    });
  });
  // Don't allow picking a date in the past
  var today = new Date();
  var iso = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  document.querySelectorAll("input[type=date]").forEach(function (i) { i.min = iso; });

  /* ---------- Animated counters ---------- */
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function runCounter(el) {
    var end = parseInt(el.getAttribute("data-count"), 10) || 0;
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduce) { el.textContent = end.toLocaleString("en-IN") + suffix; return; }
    var start = null, dur = 1600;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(end * eased).toLocaleString("en-IN") + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ---------- Reveal on scroll ---------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        en.target.querySelectorAll("[data-count]").forEach(runCounter);
        io.unobserve(en.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    document.querySelectorAll(".reveal, .stats").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); });
    document.querySelectorAll("[data-count]").forEach(runCounter);
  }

  /* ---------- Facility filters ---------- */
  document.querySelectorAll("[data-filter-group]").forEach(function (group) {
    var target = document.getElementById(group.getAttribute("data-filter-group"));
    group.querySelectorAll("button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var f = btn.getAttribute("data-filter");
        group.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
        target.querySelectorAll("[data-cat]").forEach(function (item) {
          item.classList.toggle("hide", f !== "all" && item.getAttribute("data-cat") !== f);
        });
      });
    });
  });

  /* ---------- Gallery lightbox ---------- */
  var lb = document.getElementById("lightbox");
  if (lb) {
    var items = Array.prototype.slice.call(document.querySelectorAll(".gallery button"));
    var img = lb.querySelector("img"), cap = lb.querySelector("figcaption"), idx = 0;
    function show(i) {
      idx = (i + items.length) % items.length;
      var it = items[idx];
      img.src = it.getAttribute("data-full");
      img.alt = it.querySelector("img").alt;
      cap.textContent = it.getAttribute("data-caption") + "  ·  " + (idx + 1) + " / " + items.length;
    }
    items.forEach(function (it, i) { it.addEventListener("click", function () { show(i); lb.showModal(); }); });
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(idx - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(idx + 1); });
    lb.querySelector(".lb-close").addEventListener("click", function () { lb.close(); });
    lb.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
    var tx = null;
    lb.addEventListener("touchstart", function (e) { tx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (tx === null) return;
      var dx = e.changedTouches[0].clientX - tx;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
      tx = null;
    });
  }

  /* ---------- Footer year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
