// Dr. Zende Accident Hospital — site behaviour
(function () {
  "use strict";

  var WHATSAPP_NUMBER = "918483820306";
  var TREATMENTS = {
    fracture: "Fracture Treatment",
    joint: "Joint Replacement",
    spine: "Spine Surgery",
    sports: "Sports Injury",
    trauma: "Trauma Care",
    consultation: "General Consultation"
  };

  // ---- Header: shadow on scroll, mobile menu, active link ----
  var header = document.querySelector(".site-header");
  var nav = document.getElementById("mainNav");
  var toggle = document.getElementById("navToggle");

  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    header.classList.toggle("is-scrolled", y > 10);
    // Hide the bar while scrolling down (so it doesn't cover what you're reading), show it on scroll up
    if (y < 120 || nav.classList.contains("is-open")) header.classList.remove("is-hidden");
    else if (y > lastY + 4) header.classList.add("is-hidden");
    else if (y < lastY - 4) header.classList.remove("is-hidden");
    if (Math.abs(y - lastY) > 4) lastY = y;
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  function setMenu(open) {
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    toggle.querySelector("i").className = open ? "fas fa-xmark" : "fas fa-bars";
  }
  toggle.addEventListener("click", function () { setMenu(!nav.classList.contains("is-open")); });
  nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
  document.addEventListener("click", function (e) {
    if (nav.classList.contains("is-open") && !e.target.closest("#mainNav, #navToggle")) setMenu(false);
  });

  var navLinks = Array.prototype.slice.call(nav.querySelectorAll("a"));
  if ("IntersectionObserver" in window) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (a) {
          a.classList.toggle("is-active", a.getAttribute("href") === "#" + entry.target.id);
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    navLinks.forEach(function (a) {
      var target = document.querySelector(a.getAttribute("href"));
      if (target) sectionObserver.observe(target);
    });
  }

  // ---- Reveal on scroll + stat counters ----
  var revealTargets = document.querySelectorAll(".svc, .doc, .shot, .cl-item, .book, .about-media, .about-text, .section-head, .map");
  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var suffix = el.getAttribute("data-suffix") || "";
    var start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / 1400, 1);
      var val = Math.round(target * (1 - Math.pow(1 - p, 3)));
      el.textContent = val.toLocaleString("en-IN") + (p === 1 ? suffix : "");
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if ("IntersectionObserver" in window && !reduceMotion) {
    var revealObserver = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        entry.target.querySelectorAll("[data-count]").forEach(countUp);
        obs.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    revealTargets.forEach(function (el, i) {
      el.classList.add("reveal");
      el.style.transitionDelay = (i % 4) * 70 + "ms";
      revealObserver.observe(el);
    });
  }

  // ---- Gallery filter + lightbox ----
  var tabs = document.querySelectorAll(".tab");
  var shots = Array.prototype.slice.call(document.querySelectorAll(".shot"));
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      var filter = tab.getAttribute("data-filter");
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-pressed", String(on));
      });
      shots.forEach(function (s) {
        s.hidden = filter !== "all" && s.getAttribute("data-category") !== filter;
      });
    });
  });

  var lb = document.getElementById("lightbox");
  var lbImg = document.getElementById("lbImg");
  var lbCap = document.getElementById("lbCap");
  var current = 0;
  var lastFocus = null;
  function visibleShots() { return shots.filter(function (s) { return !s.hidden; }); }
  function show(i) {
    var list = visibleShots();
    current = (i + list.length) % list.length;
    var shot = list[current];
    var img = shot.querySelector("img");
    lbImg.src = shot.getAttribute("data-full");
    lbImg.alt = img.alt;
    lbCap.textContent = shot.querySelector("strong").textContent;
  }
  function openLb(shot) {
    lastFocus = shot;
    lb.hidden = false;
    document.body.style.overflow = "hidden";
    show(visibleShots().indexOf(shot));
    document.getElementById("lbClose").focus();
  }
  function closeLb() {
    lb.hidden = true;
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }
  shots.forEach(function (s) { s.addEventListener("click", function () { openLb(s); }); });
  document.getElementById("lbClose").addEventListener("click", closeLb);
  document.getElementById("lbPrev").addEventListener("click", function () { show(current - 1); });
  document.getElementById("lbNext").addEventListener("click", function () { show(current + 1); });
  lb.addEventListener("click", function (e) { if (e.target === lb) closeLb(); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && nav.classList.contains("is-open")) setMenu(false);
    if (lb.hidden) return;
    if (e.key === "Escape") closeLb();
    if (e.key === "ArrowLeft") show(current - 1);
    if (e.key === "ArrowRight") show(current + 1);
  });

  // ---- Appointment form ----
  var form = document.getElementById("appointmentForm");
  var msg = document.getElementById("formMsg");
  var dateInput = document.getElementById("date");
  var deptSelect = document.getElementById("department");

  function todayISO() {
    var d = new Date();
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    return d.toISOString().slice(0, 10);
  }
  dateInput.min = todayISO();

  // Hero quick-book pill: preselect the treatment and jump to the form
  document.getElementById("quickBook").addEventListener("submit", function (e) {
    e.preventDefault();
    deptSelect.value = document.getElementById("quickTreatment").value;
    document.getElementById("contact").scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
    setTimeout(function () { document.getElementById("name").focus({ preventScroll: true }); }, reduceMotion ? 0 : 600);
  });

  function fail(text, field) {
    msg.textContent = text;
    msg.className = "form-msg is-error";
    if (field) { field.classList.add("is-invalid"); field.focus(); }
  }
  form.addEventListener("input", function (e) { e.target.classList.remove("is-invalid"); });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var name = document.getElementById("name");
    var phone = document.getElementById("phone");
    var message = document.getElementById("message");

    if (!name.value.trim()) return fail("Please enter your name.", name);
    var digits = phone.value.replace(/\D/g, "").slice(-10);
    if (!/^[6-9]\d{9}$/.test(digits)) return fail("Please enter a valid 10-digit mobile number.", phone);
    if (!dateInput.value) return fail("Please choose a preferred date.", dateInput);
    if (dateInput.value < todayISO()) return fail("Please choose today or a future date.", dateInput);
    if (!deptSelect.value) return fail("Please select a treatment.", deptSelect);

    var formattedDate = new Date(dateInput.value + "T00:00:00").toLocaleDateString("en-IN", {
      weekday: "long", year: "numeric", month: "long", day: "numeric"
    });
    var lines = [
      "🏥 *New Appointment Request*",
      "",
      "👤 *Patient Name:* " + name.value.trim(),
      "📞 *Phone:* " + phone.value.trim(),
      "🩺 *Treatment:* " + (TREATMENTS[deptSelect.value] || deptSelect.value),
      "📅 *Preferred Date:* " + formattedDate
    ];
    if (message.value.trim()) lines.push("💬 *Message:* " + message.value.trim());
    lines.push("", "📍 *Dr. Zende Accident Hospital, Dhule*");

    msg.textContent = "Opening WhatsApp…";
    msg.className = "form-msg is-ok";
    window.open("https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
    form.reset();
  });

  document.getElementById("year").textContent = new Date().getFullYear();
})();
