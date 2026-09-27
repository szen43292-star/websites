#!/usr/bin/env python3
"""Static site generator for Gokul Children's Hospital.

Usage:  python3 _src/build.py      (writes the .html pages into the site root)
No third-party dependencies.
"""
import json
import os
from html import escape as esc

from content import (
    SITE, FEATURES, WELCOME, TIMELINE, STATS, WHY, TEAM, REVIEWS, INSURERS, ABOUT_MORE, SONALI,
    MISSION, VISION, SERVICES_INTRO, SERVICES, FACILITY_PAGES, OTHER_FACILITIES, AYURVEDA, LACTATION, GALLERY,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = "assets/img/"
S = SITE

# ------------------------------------------------------------------ Icons (Lucide, ISC licence)
ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "map-pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "star": '<polygon fill="currentColor" stroke="none" points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "navigation": '<polygon points="3 11 22 2 13 21 11 13 3 11"/>',
    "video": '<path d="m22 8-6 4 6 4V8Z"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
    "hospital": '<path d="M12 6v4M14 14h-4M14 18h-4M14 8h-4"/><path d="M18 12h2a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2h2"/><path d="M18 22V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v18"/>',
    "stethoscope": '<path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6 6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6 6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/>',
    "flask": '<path d="M9 3h6M10 9V3M14 9V3"/><path d="M10 9 4.5 19a2 2 0 0 0 1.8 3h11.4a2 2 0 0 0 1.8-3L14 9"/><path d="M7 16h10"/>',
    "ambulance": '<path d="M10 10H6M8 8v4"/><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.28a1 1 0 0 0-.684-.948l-1.923-.641a1 1 0 0 1-.578-.502l-1.539-3.076A1 1 0 0 0 16.382 8H14"/><path d="M9 18h6"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "heart-pulse": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>',
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/>',
    "brain": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M12 5v13"/>',
    "apple": '<path d="M12 20.94c1.5 0 2.75 1.06 4 1.06 3 0 6-8 6-12.22A4.91 4.91 0 0 0 17 5c-2.22 0-4 1.44-5 2-1-.56-2.78-2-5-2a4.9 4.9 0 0 0-5 4.78C2 14 5 22 8 22c1.25 0 2.5-1.06 4-1.06Z"/><path d="M10 2c1 .5 2 2 2 5"/>',
    "eye": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    "bone": '<path d="M17 10c.7-.7 1.69 0 2.5 0a2.5 2.5 0 1 0 0-5 .5.5 0 0 1-.5-.5 2.5 2.5 0 1 0-5 0c0 .81.7 1.8 0 2.5l-7 7c-.7.7-1.69 0-2.5 0a2.5 2.5 0 0 0 0 5c.28 0 .5.22.5.5a2.5 2.5 0 1 0 5 0c0-.81-.7-1.8 0-2.5Z"/>',
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    "droplets": '<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/>',
    "virus": '<circle cx="12" cy="12" r="5"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.93 4.93l2.12 2.12M16.95 16.95l2.12 2.12M4.93 19.07l2.12-2.12M16.95 7.05l2.12-2.12"/><circle cx="10.5" cy="11" r=".6"/><circle cx="13.5" cy="13" r=".6"/>',
    "gauge": '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
    "baby": '<path d="M9 12h.01M15 12h.01"/><path d="M10 16c.5.3 1.2.5 2 .5s1.5-.2 2-.5"/><path d="M19 6.3a9 9 0 0 1 1.8 3.9 2 2 0 0 1 0 3.6 9 9 0 0 1-17.6 0 2 2 0 0 1 0-3.6A9 9 0 0 1 12 3c2 0 3.5 1.1 3.5 2.5s-.9 2.5-2 2.5c-.8 0-1.5-.4-1.5-1"/>',
    "syringe": '<path d="m18 2 4 4M17 7l3-3"/><path d="M19 9 8.7 19.3c-1 1-2.5 1-3.4 0l-.6-.6c-1-1-1-2.5 0-3.4L15 5"/><path d="m9 11 4 4M5 19l-3 3M14 4l6 6"/>',
    "pill": '<path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/>',
    "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    "microscope": '<path d="M6 18h8M3 22h18"/><path d="M14 22a7 7 0 1 0 0-14h-1M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/><path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3"/>',
    "whatsapp": '<path fill="currentColor" stroke="none" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/>',
}


def icon(name, cls="i"):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


def sprite():
    syms = "".join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items())
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{syms}</svg>'


# ------------------------------------------------------------------ Navigation
FAC_OTHER = ("Other Facilities", "facilities.html#other", "grid")
NAV = [
    ("Home", "index.html", "home", None),
    ("About", "about.html", "about", [("About Us", "about.html", "info"), ("Our Mission", "about.html#mission", "award"), ("Our Vision", "about.html#vision", "eye")]),
    ("Services", "services.html", "services", [(s["name"], s["slug"] + ".html", s["icon"]) for s in SERVICES]),
    ("Facilities", "facilities.html", "facilities", [(f["name"], f["slug"] + ".html", f["icon"]) for f in FACILITY_PAGES] + [FAC_OTHER]),
    ("Ayurveda & Lactation", "ayurveda.html", "clinic", [("Ayurveda", "ayurveda.html", "leaf"), ("Lactation", "lactation.html", "baby")]),
    ("Gallery", "gallery.html", "gallery", None),
    ("Contact", "contact.html", "contact", None),
]

DEPARTMENTS = ["General Pediatrics", "Neonatology / NICU", "Vaccination"] + [s["name"] for s in SERVICES] + ["Lactation Clinic", "Ayurveda Clinic"]

WA_LINK = f"https://wa.me/{S['whatsapp']}?text=" + "Hello%20Gokul%20Children%27s%20Hospital%2C%20I%20would%20like%20to%20book%20an%20appointment."
TEL = f"tel:{S['phone_tel']}"


def header(active):
    items = []
    for label, href, key, sub in NAV:
        cls = "nav-item" + (" has-sub" if sub else "") + (" active" if key == active else "")
        cur = ' aria-current="page"' if key == active and not sub else ""
        if sub:
            mega = " mega" if len(sub) > 6 else ""
            links = "".join(f'<li><a href="{h}"><span class="ico">{icon(ic)}</span>{esc(t)}</a></li>' for t, h, ic in sub)
            if mega:
                links += f'<li class="all"><a href="{href}">View all {esc(label.lower())} {icon("arrow-right")}</a></li>'
            items.append(f'<li class="{cls}"><a class="nav-link" href="{href}" aria-haspopup="true">{esc(label)}{icon("chevron-down")}</a><ul class="dropdown{mega}">{links}</ul></li>')
        else:
            items.append(f'<li class="{cls}"><a class="nav-link" href="{href}"{cur}>{esc(label)}</a></li>')

    m_items = []
    for n, (label, href, key, sub) in enumerate(NAV):
        if sub:
            sid = f"m-sub-{n}"
            links = f'<li><a href="{href}">All {esc(label)}</a></li>' if href not in [h for _, h, _ in sub] else ""
            links += "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for t, h, _ in sub)
            m_items.append(f'<li><button class="m-toggle" aria-expanded="false" aria-controls="{sid}">{esc(label)}{icon("chevron-down")}</button><ul class="m-sub" id="{sid}">{links}</ul></li>')
        else:
            m_items.append(f'<li><a class="m-link" href="{href}">{esc(label)}</a></li>')

    return f"""
<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar">
  <div class="container">
    <ul>
      <li><span class="pulse" aria-hidden="true"></span>24/7 Emergency: <a href="{TEL}">{S['phone_display']}</a></li>
      <li class="hide-md">{icon('mail')}<a href="mailto:{S['email']}">{S['email']}</a></li>
      <li class="hide-md">{icon('clock')}OPD: {S['hours_opd']}</li>
    </ul>
    <ul>
      <li>{icon('card')}Cashless treatment available</li>
      <li class="hide-md">{icon('map-pin')}<a href="{S['maps']}" target="_blank" rel="noopener">Get directions</a></li>
    </ul>
  </div>
</div>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="{esc(S['name'])} – home"><img src="{IMG}logo.webp" alt="Gokul Children's Hospital" width="212" height="104"></a>
    <nav class="nav" aria-label="Main"><ul>{''.join(items)}</ul></nav>
    <div class="header-cta">
      <a class="header-phone" href="{TEL}"><span class="ico">{icon('phone')}</span><span><small>Call us 24/7</small>{S['phone_display']}</span></a>
      <a class="btn btn-sm" href="contact.html#book" data-book>{icon('calendar')}Book Appointment</a>
      <a class="icon-btn call" href="{TEL}" aria-label="Call {S['phone_display']}">{icon('phone')}</a>
      <button class="icon-btn" type="button" data-open-drawer aria-controls="drawer" aria-expanded="false" aria-label="Open menu">{icon('menu')}</button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-backdrop" data-close-drawer></div>
  <div class="drawer-panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="drawer-head">
      <img src="{IMG}logo.webp" alt="Gokul Children's Hospital" width="90" height="44">
      <button class="close-btn" type="button" data-close-drawer aria-label="Close menu">{icon('x')}</button>
    </div>
    <nav class="drawer-body" aria-label="Mobile"><ul>{''.join(m_items)}</ul></nav>
    <div class="drawer-actions">
      <a class="btn btn-block" href="contact.html#book" data-book>{icon('calendar')}Book Appointment</a>
      <div class="row">
        <a class="btn btn-red btn-sm" href="{TEL}">{icon('phone')}Call</a>
        <a class="btn btn-wa btn-sm" href="{WA_LINK}" target="_blank" rel="noopener">{icon('whatsapp')}WhatsApp</a>
      </div>
    </div>
  </div>
</div>"""


def footer():
    svc = "".join(f'<li><a href="{s["slug"]}.html">{esc(s["name"])}</a></li>' for s in SERVICES[:6])
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="footer-logo" href="index.html"><img src="{IMG}logo.webp" alt="Gokul Children's Hospital" width="102" height="50" loading="lazy"></a>
        <p>Dr. Parikshit Pundalik Deore is a renowned Pediatrician and Neonatologist in Dhule and has been practicing since 2011.</p>
        <a href="about.html" class="link-arrow" style="color:#fff">Read more {icon('arrow-right')}</a>
        <div><span class="emergency-chip"><span class="pulse" aria-hidden="true"></span>Open {S['hours_hospital']}</span></div>
      </div>
      <div>
        <h3>Quick Links</h3>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="about.html">About Us</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="facilities.html">Facilities</a></li>
          <li><a href="ayurveda.html">Ayurveda &amp; Lactation</a></li>
          <li><a href="gallery.html">Gallery</a></li>
          <li><a href="contact.html">Contact Us</a></li>
        </ul>
      </div>
      <div>
        <h3>Specialities</h3>
        <ul>{svc}<li><a href="services.html">All services →</a></li></ul>
      </div>
      <div>
        <h3>Hospital Address</h3>
        <ul class="f-contact">
          <li>{icon('map-pin')}<a href="{S['maps']}" target="_blank" rel="noopener">{S['address_1']},<br>{S['address_2']}</a></li>
          <li>{icon('phone')}<a href="{TEL}">{S['phone_display']}</a></li>
          <li>{icon('mail')}<span><a href="mailto:{S['email']}">{S['email']}</a><br><a href="mailto:{S['email_2']}">{S['email_2']}</a></span></li>
          <li>{icon('clock')}<span>Hospital: {S['hours_hospital']}<br>OPD: {S['hours_opd']}</span></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>Copyright © <span data-year>2026</span> Gokul Children's Hospital. All rights reserved.</span>
      <span>Pediatrics &amp; Neonatology Center · Dhule, Maharashtra</span>
    </div>
  </div>
</footer>
<nav class="action-bar" aria-label="Quick actions">
  <a class="call" href="{TEL}">{icon('phone')}Call</a>
  <a class="wa" href="{WA_LINK}" target="_blank" rel="noopener">{icon('whatsapp')}WhatsApp</a>
  <a href="{S['maps']}" target="_blank" rel="noopener">{icon('navigation')}Directions</a>
  <a class="book" href="contact.html#book" data-book>{icon('calendar')}Book</a>
</nav>
<a class="wa-float" href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">{icon('whatsapp')}</a>
{booking_modal()}"""


def booking_form(ctx="m", email_option=False, include_subject=False):
    opts = "".join(f"<option>{esc(d)}</option>" for d in DEPARTMENTS)
    subj = f"""<div class="field"><label for="{ctx}-subject">Subject <span class="opt">(optional)</span></label><input id="{ctx}-subject" name="subject" type="text" placeholder="e.g. Appointment request"></div>""" if include_subject else ""
    email = f"""<div class="field"><label for="{ctx}-email">Email <span class="opt">(optional)</span></label><input id="{ctx}-email" name="email" type="email" autocomplete="email"></div>""" if include_subject else ""
    actions = (f"""<div class="form-actions"><button class="btn btn-wa" type="submit" value="whatsapp">{icon('whatsapp')}Send on WhatsApp</button><button class="btn btn-ghost" type="submit" value="email">{icon('mail')}Send by Email</button></div>"""
               if email_option else f"""<button class="btn btn-wa btn-block" type="submit" value="whatsapp">{icon('whatsapp')}Send request on WhatsApp</button>""")
    return f"""
<form class="form" data-enquiry novalidate>
  <div class="row">
    <div class="field"><label for="{ctx}-parent">Parent / guardian name</label><input id="{ctx}-parent" name="parent" type="text" autocomplete="name" required></div>
    <div class="field"><label for="{ctx}-phone">Mobile number</label><input id="{ctx}-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" pattern="[0-9+ ()-]{{10,}}" required placeholder="10-digit mobile"></div>
  </div>
  <div class="row">
    <div class="field"><label for="{ctx}-child">Child's name <span class="opt">(optional)</span></label><input id="{ctx}-child" name="child" type="text"></div>
    <div class="field"><label for="{ctx}-age">Child's age <span class="opt">(optional)</span></label><input id="{ctx}-age" name="age" type="text" placeholder="e.g. 8 months"></div>
  </div>
  {email}
  <div class="row">
    <div class="field"><label for="{ctx}-dept">Department</label><select id="{ctx}-dept" name="department">{opts}</select></div>
    <div class="field"><label for="{ctx}-date">Preferred date <span class="opt">(optional)</span></label><input id="{ctx}-date" name="date" type="date"></div>
  </div>
  <fieldset class="field">
    <legend>Consultation type</legend>
    <div class="seg">
      <label><input type="radio" name="visit" value="In-person visit" checked><span>{icon('hospital')}In-person</span></label>
      <label><input type="radio" name="visit" value="Video call"><span>{icon('video')}Video call</span></label>
      <label><input type="radio" name="visit" value="Audio call"><span>{icon('phone')}Audio call</span></label>
    </div>
  </fieldset>
  {subj}
  <div class="field"><label for="{ctx}-msg">Message <span class="opt">(optional)</span></label><textarea id="{ctx}-msg" name="message" rows="3" placeholder="Symptoms or anything we should know"></textarea></div>
  {actions}
  <p class="form-note">OPD consultations: {S['hours_opd']}. For emergencies please call <a href="{TEL}">{S['phone_display']}</a> right away.</p>
</form>"""


def booking_modal():
    return f"""
<dialog class="modal" id="book-modal" aria-labelledby="book-title">
  <div class="modal-head">
    <div><h2 id="book-title">Book an appointment</h2><p>Fill in a few details and send them to us on WhatsApp — we'll confirm your slot.</p></div>
    <button class="close-btn" type="button" data-close-modal aria-label="Close">{icon('x')}</button>
  </div>
  <div class="modal-body">{booking_form("m")}</div>
</dialog>"""


def jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": ["Hospital", "MedicalClinic"],
        "name": S["name"],
        "alternateName": "Gokul Children's Hospital Pediatrics and Neonatology Center",
        "url": S["url"],
        "logo": S["url"] + "/assets/img/logo.png",
        "image": S["url"] + "/assets/img/gallery/fdxf3jpioq.webp",
        "telephone": S["phone_tel"],
        "email": S["email"],
        "medicalSpecialty": ["Pediatric", "Neonatal"],
        "address": {"@type": "PostalAddress", "streetAddress": S["address_1"], "addressLocality": "Dhule", "addressRegion": "Maharashtra", "postalCode": "424001", "addressCountry": "IN"},
        "geo": {"@type": "GeoCoordinates", "latitude": S["lat"], "longitude": S["lng"]},
        "openingHours": "Mo-Su 00:00-23:59",
        "founder": {"@type": "Physician", "name": "Dr. Parikshit Pundalik Deore"},
        "foundingDate": "2011",
    }
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def page(filename, title, description, active, body, schema=False):
    full_title = f"{title} | {S['name']}, Dhule" if filename != "index.html" else f"{S['name']} Dhule | Pediatrician & Neonatologist, NICU & PICU"
    html = f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#4f2d83">
<link rel="canonical" href="{S['url']}/{'' if filename == 'index.html' else filename}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{S['url']}/assets/img/gallery/fdxf3jpioq.webp">
<link rel="icon" type="image/png" href="{IMG}favicon.png">
<link rel="apple-touch-icon" href="{IMG}favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{jsonld() if schema else ''}
</head>
<body>
{sprite()}
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename)


# ------------------------------------------------------------------ Shared blocks
def crumbs(trail):
    parts = ['<li><a href="index.html">Home</a></li>']
    for i, (t, h) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f'<li><span aria-current="page">{esc(t)}</span></li>')
        else:
            parts.append(f'<li><a href="{h}">{esc(t)}</a></li>')
    return f'<nav aria-label="Breadcrumb"><ol class="crumbs">{"".join(parts)}</ol></nav>'


def page_hero(trail, eyebrow, h1, lead="", buttons=True, dept=""):
    btns = ""
    if buttons:
        btns = f"""<div class="btn-row">
      <a class="btn" href="contact.html#book" data-book="{esc(dept)}">{icon('calendar')}Book Appointment</a>
      <a class="btn btn-ghost" href="{TEL}">{icon('phone')}{S['phone_display']}</a>
    </div>"""
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f"""
<section class="page-hero">
  <div class="container">
    {crumbs(trail)}
    <p class="eyebrow">{esc(eyebrow)}</p>
    <h1>{h1}</h1>
    {lead_html}
    {btns}
  </div>
</section>"""


def checks(items, variant="chips"):
    cls = {"chips": "checks chips", "two": "checks two", "plain": "checks"}[variant]
    return f'<ul class="{cls}">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def render_sections(sections):
    out = []
    for sec in sections:
        if sec.get("h"):
            out.append(f'<h2>{esc(sec["h"])}</h2>')
        for p in sec.get("paras", []):
            out.append(f"<p>{esc(p)}</p>")
        if "list" in sec:
            out.append(checks(sec["list"], "two" if sec.get("two") else "plain" if sec.get("plain") else "chips"))
        if "cards" in sec:
            out.append('<div class="expertise">' + "".join(f"<div><strong>{esc(a)}</strong><span>{esc(b)}</span></div>" for a, b in sec["cards"]) + "</div>")
    return "\n".join(out)


def help_box(dept=""):
    return f"""
<div class="help-box">
  <h3>Let's help you!</h3>
  <ul>
    <li>{icon('map-pin')}<span>{S['address_1']}, {S['address_2']}</span></li>
    <li>{icon('mail')}<a href="mailto:{S['email']}">{S['email']}</a></li>
    <li>{icon('phone')}<a href="{TEL}">{S['phone_display']}</a></li>
    <li>{icon('clock')}<span>OPD: {S['hours_opd']}<br>Emergency: 24/7</span></li>
  </ul>
  <a class="btn btn-light" href="contact.html#book" data-book="{esc(dept)}">{icon('calendar')}Book Appointment</a>
  <a class="btn btn-wa" href="{WA_LINK}" target="_blank" rel="noopener">{icon('whatsapp')}WhatsApp us</a>
</div>"""


def aside_nav(title, links, current):
    cur = ' aria-current="page"'
    lis = "".join(
        f'<li><a href="{h}"{cur if h == current else ""}>{icon(ic)}{esc(t)}</a></li>' for t, h, ic in links
    )
    return f'<div class="aside-box"><h3>{esc(title)}</h3><ul class="aside-nav">{lis}</ul></div>'


def service_cards(limit=None, cls="grid grid-5"):
    cards = []
    for s in SERVICES[:limit]:
        cards.append(f"""
<a class="card card-link service-card reveal" href="{s['slug']}.html">
  <span class="ico {s['tint']}">{icon(s['icon'])}</span>
  <h3>{esc(s['name'])}</h3>
  <p>{esc(s['summary'])}</p>
  <span class="link-arrow">Read more {icon('arrow-right')}</span>
</a>""")
    return f'<div class="{cls}">' + "".join(cards) + "</div>"


def stats_block():
    items = "".join(
        f'<div class="stat"><strong data-count="{n}" data-suffix="{suf}">{n:,}{suf}</strong><span>{esc(lbl)}</span></div>' for n, suf, lbl in STATS
    )
    return f'<div class="stats" role="list" aria-label="Hospital in numbers">{items}</div>'


def why_block():
    items = "".join(
        f'<div class="why-item reveal"><span class="ico {t}">{icon(ic)}</span><div><h3>{esc(h)}</h3><p>{esc(p)}</p></div></div>'
        for ic, t, h, p in WHY["items"]
    )
    return f"""
<section class="section">
  <div class="container split">
    <div class="media-frame reveal">
      <img src="{IMG}why.webp" alt="Gokul Children's Hospital building, Dhule" width="1600" height="1051" loading="lazy">
      <div class="badge-years"><strong>24/7</strong><span>NICU, PICU &amp; emergency care</span></div>
    </div>
    <div>
      <p class="eyebrow">Why choose us</p>
      <h2>{esc(WHY['title'])}</h2>
      <p>{esc(WHY['intro'])}</p>
      <div class="why-list">{items}</div>
      <div class="btn-row" style="margin-top:24px">
        <a class="btn btn-wa" href="{WA_LINK}" target="_blank" rel="noopener">{icon('whatsapp')}WhatsApp now</a>
        <a class="btn btn-ghost" href="nicu.html">About our NICU {icon('arrow-right')}</a>
      </div>
    </div>
  </div>
</section>"""


def cta_band():
    return f"""
<section class="section-tight">
  <div class="container">
    <div class="cta-band reveal">
      <div>
        <h2>Your child's health is our priority.</h2>
        <p>Book an in-person visit or a video / audio consultation. Emergency care is available 24 hours, every day.</p>
      </div>
      <div class="btn-row">
        <a class="btn btn-light" href="contact.html#book" data-book>{icon('calendar')}Book Appointment</a>
        <a class="btn btn-outline-light" href="{TEL}">{icon('phone')}{S['phone_display']}</a>
      </div>
    </div>
  </div>
</section>"""


def insurance_block():
    logos = "".join(f'<li><img src="{IMG}insurance/{f}.webp" alt="{esc(n)}" width="167" height="76" loading="lazy"></li>' for f, n in INSURERS)
    return f"""
<section class="section-tight">
  <div class="container">
    <div class="cashless reveal">
      <div class="cashless-head">
        <div><p class="eyebrow">Insurance accepted</p><h2>Cashless Treatment Facilities Available</h2></div>
        <a class="btn btn-ghost" href="{TEL}">{icon('phone')}Ask about your policy</a>
      </div>
      <ul class="logos">{logos}</ul>
    </div>
  </div>
</section>"""


def contact_tiles():
    return f"""
<div class="contact-band">
  <a class="contact-tile reveal" href="{TEL}"><span class="ico t-red">{icon('phone')}</span><span><small>Have a question? Call us now</small><strong>{S['phone_display']}</strong></span></a>
  <a class="contact-tile reveal" href="mailto:{S['email']}"><span class="ico t-purple">{icon('mail')}</span><span><small>Need support? Drop us an email</small><strong>{S['email']}</strong></span></a>
  <a class="contact-tile reveal" href="{S['maps']}" target="_blank" rel="noopener"><span class="ico t-teal">{icon('map-pin')}</span><span><small>Visit us</small><strong>{S['address_1']}, Dhule</strong></span></a>
  <div class="contact-tile reveal"><span class="ico t-sun">{icon('clock')}</span><span><small>We are open on</small><strong>{S['hours_hospital']}</strong></span></div>
</div>"""


# ------------------------------------------------------------------ Pages
def build_home():
    feats = ""
    for ic, t, h, p in FEATURES:
        extra = f'<a href="{TEL}">{icon("phone")}Call {S["phone_display"]}</a>' if h == "Emergency" else ""
        feats += f'<div class="feature{" emergency" if h == "Emergency" else ""}"><span class="ico {t}">{icon(ic)}</span><h3>{h}</h3><p>{esc(p)}</p>{extra}</div>'

    timeline = "".join(f"<li><strong>{y}</strong>{esc(t)}</li>" for y, t in TIMELINE)

    fac_cards = ""
    for f in FACILITY_PAGES:
        fac_cards += f"""
<a class="photo-card reveal" href="{f['slug']}.html">
  <div class="ph"><img src="{IMG}{f['img']}" alt="{esc(f['name'])}" width="651" height="417" loading="lazy"></div>
  <div class="body"><span class="tag">Neonatology &amp; Pediatrics</span><h3>{esc(f['name'])}</h3><p>{esc(f['summary'])}</p><span class="link-arrow">Learn more {icon('arrow-right')}</span></div>
</a>"""
    others = "".join(
        f'<a class="mini-facility reveal" href="facilities.html#other"><span class="ico {t}">{icon(ic)}</span><span><strong>{esc(n)}</strong><span>Other facilities</span></span></a>'
        for (n, _, ic), t in zip(OTHER_FACILITIES, ["t-purple", "t-teal", "t-red", "t-sun", "t-pink"])
    )

    team = "".join(
        f'<article class="doc reveal"><div class="ph"><img src="{IMG}{img}" alt="{esc(n)}" width="600" height="600" loading="lazy"></div><div class="body"><h3>{esc(n)}</h3><p class="deg">{esc(d)}</p><p>{esc(r)}</p></div></article>'
        for img, n, d, r in TEAM
    )

    stars5 = f'<span class="stars" aria-label="5 out of 5 stars">{icon("star") * 5}</span>'
    reviews = "".join(
        f'<figure class="review reveal">{stars5}<blockquote>{esc(t)}</blockquote><figcaption class="who"><span class="av" style="background:{c}">{n[0]}</span><span><strong>{esc(n)}</strong><small>Posted on Google</small></span></figcaption></figure>'
        for n, t, c in REVIEWS
    )

    body = f"""
<section class="hero">
  <span class="balloon b1"></span><span class="balloon b2"></span><span class="balloon b3"></span>
  <div class="container">
    <div>
      <span class="pill"><b>2011</b>Pediatrics &amp; Neonatology Center · Dhule</span>
      <h1>Trust the experts for the best <span class="hl">Neonatal &amp; Pediatric</span> care.</h1>
      <p class="lead">Welcome to Gokul Children's Hospital in Dhule, Maharashtra — led by Dr. Parikshit Pundalik Deore, Pediatrician &amp; Neonatologist, with an experienced team of doctors for pediatric and neonatal care.</p>
      <div class="btn-row">
        <a class="btn" href="contact.html#book" data-book>{icon('calendar')}Book Appointment</a>
        <a class="btn btn-ghost" href="{TEL}">{icon('phone')}Call {S['phone_display']}</a>
      </div>
      <ul class="hero-badges">
        <li>{icon('shield')}24/7 emergency &amp; trauma</li>
        <li>{icon('baby')}Modular NICU &amp; PICU</li>
        <li>{icon('card')}Cashless treatment</li>
      </ul>
    </div>
    <div class="hero-visual" aria-hidden="false">
      <div class="main"><img src="{IMG}gallery/0buorr662g.webp" alt="Modular NICU at Gokul Children's Hospital" width="1600" height="1067" fetchpriority="high"></div>
      <div class="sub"><img src="{IMG}gallery/fdxf3jpioq.webp" alt="Gokul Children's Hospital building on Malegaon Road, Dhule" width="985" height="675"></div>
      <div class="float-card fc-1"><span class="ico">{icon('ambulance')}</span><span><strong>24 hours emergency</strong>Fully equipped trauma centre</span></div>
      <div class="float-card fc-2"><span class="ico t-purple">{icon('star')}</span><span><strong>Excellent</strong>{stars5}<br><small>Based on 12 Google reviews</small></span></div>
    </div>
  </div>
</section>

<section class="features">
  <div class="container">
    <div class="features-grid">{feats}</div>
    <nav class="quick" aria-label="Popular">
      <a href="nicu.html">{icon('baby')}NICU</a>
      <a href="vaccination.html#schedule">{icon('syringe')}Vaccination schedule</a>
      <a href="services.html">{icon('stethoscope')}All specialities</a>
      <a href="lactation.html">{icon('heart')}Lactation clinic</a>
      <a href="ayurveda.html">{icon('leaf')}Ayurveda clinic</a>
      <a href="{S['maps']}" target="_blank" rel="noopener">{icon('navigation')}Directions</a>
    </nav>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="media-frame reveal">
      <img src="{IMG}gallery/k4a6k9qggy.webp" alt="Dr. Parikshit Pundalik Deore in his consultation room" width="1600" height="1067" loading="lazy">
      <div class="badge-years"><strong>12+ yrs</strong><span>Serving newborns &amp; children since 2011</span></div>
    </div>
    <div>
      <p class="eyebrow">Welcome to</p>
      <h2>Gokul Children's Hospital in Dhule, Maharashtra.</h2>
      <p>{esc(WELCOME[0])}</p>
      <p>His expertise is complemented by a team of dedicated healthcare professionals at Gokul Children's Hospital.</p>
      <ol class="timeline" aria-label="Dr. Deore's education and training">{timeline}</ol>
      <div class="btn-row">
        <a class="btn" href="about.html">Read more {icon('arrow-right')}</a>
        <a class="btn btn-ghost" href="contact.html#book" data-book>{icon('video')}Video / audio consult</a>
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">{stats_block()}</div>
</section>

<section class="section bg-soft">
  <div class="container">
    <div class="section-head center">
      <p class="eyebrow">Our services</p>
      <h2>Our Specialities</h2>
      <p class="lead">{esc(SERVICES_INTRO)}</p>
    </div>
    {service_cards()}
    <div class="btn-row" style="justify-content:center;margin-top:36px"><a class="btn btn-ghost" href="services.html">View all services {icon('arrow-right')}</a></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Facilities</p>
      <h2>Neonatology &amp; Pediatrics</h2>
      <p class="lead">Everything your child may need under one roof — from a fully modular NICU to super-specialist OPDs.</p>
    </div>
    <div class="grid grid-4">{fac_cards}</div>
    <div class="grid grid-5" style="margin-top:20px">{others}</div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="clinic reveal">
      <div class="clinic-media"><img src="{IMG}gallery/wa-17.22.04.webp" alt="Dr. Sonali Parikshit Deore at the Gokul Ayurveda &amp; Lactation Clinic" width="1600" height="900" loading="lazy"></div>
      <div class="clinic-body">
        <p class="eyebrow">New · Ayurveda &amp; Lactation Clinic</p>
        <h2>Care for mothers, too.</h2>
        <p>Led by <strong>{SONALI['name']}</strong> — BAMS, MBA in Hospital Management, Diploma in Counselling Psychology, ACLP (Lactation Counsellor) and Diploma in Yoga Science.</p>
        <div class="cols">
          <div class="col t-teal"><h3>{icon('baby')}Lactation</h3><p>Breastfeeding guidance, latch support, low milk supply, weaning and online consultations.</p></div>
          <div class="col t-sun"><h3>{icon('leaf')}Ayurveda</h3><p>Panchakarma, Shirodhara, Ayurvedic lifestyle &amp; yoga guidance.</p></div>
        </div>
        <div class="btn-row">
          <a class="btn btn-teal" href="lactation.html">Lactation clinic {icon('arrow-right')}</a>
          <a class="btn btn-ghost" href="ayurveda.html">Ayurveda clinic {icon('arrow-right')}</a>
        </div>
      </div>
    </div>
  </div>
</section>

{why_block()}

<section class="section bg-teal">
  <div class="container">
    <div class="section-head center">
      <p class="eyebrow">Our doctors</p>
      <h2>Meet Our Team</h2>
    </div>
    <div class="grid grid-4 grid-team">{team}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="reviews-head">
      <div class="section-head" style="margin:0">
        <p class="eyebrow">Testimonials</p>
        <h2>What our patients say</h2>
        <p class="lead" style="margin:0">We are very honest, careful and diligent in our work and treat our patients with utmost care.</p>
      </div>
      <a class="rating-box" href="{S['maps']}" target="_blank" rel="noopener" style="text-decoration:none">
        <span class="g">G</span>
        <span><strong>EXCELLENT</strong> {stars5}<small>Based on 12 reviews · Check all Google reviews →</small></span>
      </a>
    </div>
    <div class="grid grid-4">{reviews}</div>
  </div>
</section>

{insurance_block()}

<section class="section-tight">
  <div class="container">{contact_tiles()}</div>
</section>

{cta_band()}
"""
    page("index.html", "Home",
         "Gokul Children's Hospital, Dhule – Pediatrician & Neonatologist Dr. Parikshit Pundalik Deore. Modular NICU & PICU, 24/7 emergency, vaccination, pediatric super-specialities and cashless treatment.",
         "home", body, schema=True)


def build_about():
    timeline = "".join(f"<li><strong>{y}</strong>{esc(t)}</li>" for y, t in TIMELINE)
    body = f"""
{page_hero([("About Us", "about.html")], "About us", "Gokul Children's Hospital, Dhule, Maharashtra", "A state-of-the-art children's hospital on Malegaon Road, Dhule — caring for newborns, infants, children and adolescents since 2011.")}

<section class="section">
  <div class="container">
    <div class="lead-doc reveal">
      <img src="{IMG}gallery/k4a6k9qggy.webp" alt="Dr. Parikshit Pundalik Deore" width="600" height="600" loading="lazy">
      <div>
        <p class="eyebrow">Pediatrician &amp; Neonatologist</p>
        <h2>Dr. Parikshit Pundalik Deore</h2>
        <ul class="cred"><li>MBBS 2003</li><li>MD 2009</li><li>PGPN, Boston USA 2017</li><li>ENS, Munich 2020</li><li>IPPN, Munich 2023</li></ul>
        {''.join(f'<p>{esc(p)}</p>' for p in WELCOME)}
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container split">
    <div>
      <p class="eyebrow">Our hospital</p>
      <h2>Care that fits your family's day.</h2>
      {''.join(f'<p>{esc(p)}</p>' for p in ABOUT_MORE[:3])}
    </div>
    <div class="grid" style="gap:14px">
      <div class="why-item reveal"><span class="ico t-purple">{icon('clock')}</span><div><h3>Consultation hours</h3><p>{S['hours_opd']}. Emergency care 24/7.</p></div></div>
      <div class="why-item reveal"><span class="ico t-teal">{icon('video')}</span><div><h3>In-person &amp; virtual</h3><p>In-person visits and virtual consultations through video and audio calls.</p></div></div>
      <div class="why-item reveal"><span class="ico t-pink">{icon('card')}</span><div><h3>Insurance accepted</h3><p>Cashless treatment facilities available with leading insurers and TPAs.</p></div></div>
      <div class="why-item reveal"><span class="ico t-sun">{icon('calendar')}</span><div><h3>Easy online booking</h3><p>Request your appointment in under a minute on WhatsApp.</p></div></div>
      <a class="btn" href="contact.html#book" data-book>{icon('calendar')}Book Appointment</a>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="callout reveal">{icon('heart')}<p>{esc(ABOUT_MORE[3])}</p></div>
  </div>
</section>

<section class="section-tight">
  <div class="container">{stats_block()}</div>
</section>

<section class="section bg-soft" id="sonali">
  <div class="container split reverse">
    <div class="media-frame reveal">
      <img src="{IMG}gallery/wa-17.22.01.webp" alt="{SONALI['name']} at the Gokul Ayurveda &amp; Lactation Clinic" width="1600" height="900" loading="lazy">
    </div>
    <div>
      <p class="eyebrow">Ayurveda &amp; Lactation Clinic</p>
      <h2>About {SONALI['name']}</h2>
      <ul class="cred">{''.join(f'<li>{esc(c)}</li>' for c in SONALI['creds'])}</ul>
      <p>{esc(SONALI['lactation'])}</p>
      <p>{esc(SONALI['ayurveda'])}</p>
      <div class="btn-row"><a class="btn btn-teal" href="lactation.html">Lactation clinic {icon('arrow-right')}</a><a class="btn btn-ghost" href="ayurveda.html">Ayurveda clinic {icon('arrow-right')}</a></div>
    </div>
  </div>
</section>

<section class="section" id="mission">
  <div class="container split">
    <div class="media-frame reveal"><img src="{IMG}mission.webp" alt="" width="700" height="450" loading="lazy"></div>
    <div>
      <p class="eyebrow">Our mission</p>
      <h2>Specialized care for every child, at an affordable price.</h2>
      <p>{esc(MISSION)}</p>
    </div>
  </div>
</section>

<section class="section-tight" id="vision">
  <div class="container split reverse">
    <div class="media-frame reveal"><img src="{IMG}vision.webp" alt="" width="768" height="572" loading="lazy"></div>
    <div>
      <p class="eyebrow">Our vision</p>
      <h2>A healthy start in life for every child.</h2>
      {''.join(f'<p>{esc(p)}</p>' for p in VISION)}
    </div>
  </div>
</section>

{why_block()}
{cta_band()}
"""
    page("about.html", "About Us",
         "About Gokul Children's Hospital, Dhule and Dr. Parikshit Pundalik Deore, Pediatrician & Neonatologist since 2011. Our mission, vision and the Ayurveda & Lactation Clinic by Dr. Sonali Deore.",
         "about", body)


def build_services():
    body = f"""
{page_hero([("Services", "services.html")], "Our services", "Our Specialities", esc(SERVICES_INTRO))}
<section class="section">
  <div class="container">
    {service_cards(cls="grid grid-3")}
  </div>
</section>
{insurance_block()}
{cta_band()}
"""
    page("services.html", "Services & Specialities",
         "Pediatric super-specialities at Gokul Children's Hospital, Dhule: surgery, cardiology, neurology, gastroenterology, ophthalmology, orthopedics, urology, infectious diseases, hematology and endocrinology.",
         "services", body)

    svc_links = [(s["name"], s["slug"] + ".html", s["icon"]) for s in SERVICES]
    for s in SERVICES:
        content = "".join(f"<p>{esc(p)}</p>" for p in s["paras"]) + render_sections(s["sections"])
        body = f"""
{page_hero([("Services", "services.html"), (s["name"], "")], s["name"], esc(s["h1"]), "", dept=s["name"])}
<section class="section">
  <div class="container with-aside">
    <article class="prose">
      <img class="banner" src="{IMG}{s['banner']}" alt="{esc(s['name'])} at Gokul Children's Hospital" width="1600" height="469">
      {content}
      <div class="callout">{icon('info')}<p>Not sure which specialist your child needs? Call <a href="{TEL}">{S['phone_display']}</a> or <a href="{WA_LINK}" target="_blank" rel="noopener">message us on WhatsApp</a> and we'll guide you.</p></div>
    </article>
    <aside class="aside">
      {aside_nav("Our services", svc_links, s["slug"] + ".html")}
      {help_box(s["name"])}
    </aside>
  </div>
</section>
"""
        page(s["slug"] + ".html", s["name"], f"{s['name']} at Gokul Children's Hospital, Dhule, Maharashtra. {s['summary']}", "services", body)


def build_facilities():
    cards = ""
    for f in FACILITY_PAGES:
        cards += f"""
<a class="photo-card" data-cat="neo" href="{f['slug']}.html">
  <div class="ph"><img src="{IMG}{f['img']}" alt="{esc(f['name'])}" width="651" height="417" loading="lazy"></div>
  <div class="body"><span class="tag">Neonatology &amp; Pediatrics</span><h3>{esc(f['name'])}</h3><p>{esc(f['summary'])}</p><span class="link-arrow">Learn more {icon('arrow-right')}</span></div>
</a>"""
    for n, img, ic in OTHER_FACILITIES:
        cards += f"""
<div class="photo-card static" data-cat="other">
  <div class="ph"><img src="{IMG}{img}" alt="{esc(n)}" width="300" height="192" loading="lazy"></div>
  <div class="body"><span class="tag">Other facilities</span><h3>{esc(n)}</h3></div>
</div>"""
    body = f"""
{page_hero([("Facilities", "facilities.html")], "Facilities", "Our Facilities", "A fully modular NICU, round-the-clock emergency, pharmacy, pathology &amp; radiology, and a modular operation theatre — all designed around children.")}
<section class="section" id="other">
  <div class="container">
    <div class="filters" role="group" aria-label="Filter facilities" data-filter-group="fac-grid">
      <button type="button" data-filter="all" aria-pressed="true">All</button>
      <button type="button" data-filter="neo" aria-pressed="false">Neonatology &amp; Pediatrics</button>
      <button type="button" data-filter="other" aria-pressed="false">Other Facilities</button>
    </div>
    <div class="grid grid-3" id="fac-grid">{cards}</div>
  </div>
</section>
{cta_band()}
"""
    page("facilities.html", "Facilities",
         "Facilities at Gokul Children's Hospital, Dhule: modular NICU, vaccination, pediatric & neonatal surgeries, super-specialist OPDs, modular OT, 24-hour pharmacy, emergency, canteen, pathology & radiology.",
         "facilities", body)

    fac_links = [(f["name"], f["slug"] + ".html", f["icon"]) for f in FACILITY_PAGES] + [FAC_OTHER]
    for f in FACILITY_PAGES:
        content = "".join(f"<p>{esc(p)}</p>" for p in f["paras"])
        content += render_sections(f["sections"])
        if f.get("schedule"):
            rows = "".join(
                f'<li><span class="age">{esc(a)}</span><span class="vx">{"".join(f"<span>{esc(v)}</span>" for v in vs)}</span></li>' for a, vs in f["schedule"]
            )
            content += f'<h2 id="schedule">Vaccination schedule</h2><ol class="schedule">{rows}</ol>'
            content += f'<div class="callout">{icon("syringe")}<p>Not sure which dose is due? Bring your child\'s vaccination card and we\'ll guide you — or <a href="{WA_LINK}" target="_blank" rel="noopener">ask us on WhatsApp</a>.</p></div>'
        body = f"""
{page_hero([("Facilities", "facilities.html"), (f["name"], "")], "Neonatology & Pediatrics", esc(f["full"]), "", dept="Vaccination" if f["slug"] == "vaccination" else ("Neonatology / NICU" if f["slug"] == "nicu" else ""))}
<section class="section">
  <div class="container with-aside">
    <article class="prose">
      <img class="banner" src="{IMG}{f['img']}" alt="{esc(f['name'])} at Gokul Children's Hospital" width="651" height="417">
      {content}
    </article>
    <aside class="aside">
      {aside_nav("Neonatology & Pediatrics", fac_links, f["slug"] + ".html")}
      {help_box()}
    </aside>
  </div>
</section>
"""
        page(f["slug"] + ".html", f["name"], f"{f['full']} at Gokul Children's Hospital, Dhule. {f['summary']}", "facilities", body)


def build_clinics():
    clinic_links = [("Ayurveda", "ayurveda.html", "leaf"), ("Lactation", "lactation.html", "baby")]
    ayur = f"""
{page_hero([("Ayurveda & Lactation", "ayurveda.html"), ("Ayurveda", "")], "Gokul Ayurveda & Lactation Clinic", "Ayurveda", f"Holistic Ayurvedic care and Panchakarma treatments by {SONALI['name']} (BAMS, Diploma in Yoga Science).", dept="Ayurveda Clinic")}
<section class="section">
  <div class="container with-aside">
    <article class="prose">
      <img class="banner" src="{IMG}ayurveda.webp" alt="Ayurveda" width="1024" height="575">
      <h2>1. Panchakarma</h2>
      {checks(AYURVEDA['panchakarma'])}
      <h2>2. Ayurvedic lifestyle guidance</h2>
      <p>Personalised Ayurvedic lifestyle and yoga guidance for everyday health and well-being.</p>
      <h2>3. Guidance for</h2>
      {checks(AYURVEDA['guidance'])}
    </article>
    <aside class="aside">
      {aside_nav("Ayurveda & Lactation", clinic_links, "ayurveda.html")}
      {help_box("Ayurveda Clinic")}
    </aside>
  </div>
</section>
"""
    page("ayurveda.html", "Ayurveda Clinic",
         "Gokul Ayurveda Clinic, Dhule: Panchakarma (Snehana, Swedana, Vamana, Virechana, Nasya, Shirodhara and more), Ayurvedic lifestyle guidance and yoga guidance by Dr. Sonali Parikshit Deore.",
         "clinic", ayur)

    items = "".join(
        f'<div class="why-item reveal"><span class="ico {["t-teal","t-purple","t-pink","t-sun"][i % 4]}">{icon("check")}</span><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></div>'
        for i, (t, d) in enumerate(LACTATION)
    )
    lact = f"""
{page_hero([("Ayurveda & Lactation", "ayurveda.html"), ("Lactation", "")], "Gokul Ayurveda & Lactation Clinic", "Lactation Clinic", f"Breastfeeding support for new mothers by {SONALI['name']}, ACLP (Lactation Counsellor) — in person or online.", dept="Lactation Clinic")}
<section class="section">
  <div class="container with-aside">
    <article class="prose">
      <img class="banner" src="{IMG}lactation.webp" alt="Mother breastfeeding her baby" width="1024" height="512">
      <h2>Our key services</h2>
      <div class="grid grid-2" style="gap:14px">{items}</div>
    </article>
    <aside class="aside">
      {aside_nav("Ayurveda & Lactation", clinic_links, "lactation.html")}
      {help_box("Lactation Clinic")}
    </aside>
  </div>
</section>
"""
    page("lactation.html", "Lactation Clinic",
         "Lactation Clinic at Gokul Children's Hospital, Dhule: breastfeeding guidance, latch support, low milk supply, weaning guidance, mother support groups and online lactation consultation.",
         "clinic", lact)


def build_gallery():
    items = "".join(
        f'<button type="button" data-full="{IMG}{src}" data-caption="{esc(cap)}" aria-label="Open image: {esc(cap)}"><img src="{IMG}{src}" alt="{esc(cap)}" loading="lazy"></button>'
        for src, cap in GALLERY
    )
    body = f"""
{page_hero([("Gallery", "gallery.html")], "Gallery", "Take a look inside", "Our NICU, reception, consultation rooms and the new Gokul Ayurveda &amp; Lactation Clinic.", buttons=False)}
<section class="section">
  <div class="container"><div class="gallery">{items}</div></div>
</section>
<dialog class="lightbox" id="lightbox" aria-label="Image viewer">
  <button class="lb-btn lb-close" type="button" aria-label="Close">{icon('x')}</button>
  <button class="lb-btn lb-prev" type="button" aria-label="Previous image">{icon('arrow-right')}</button>
  <button class="lb-btn lb-next" type="button" aria-label="Next image">{icon('arrow-right')}</button>
  <figure><img src="" alt=""><figcaption></figcaption></figure>
</dialog>
{cta_band()}
"""
    page("gallery.html", "Gallery", "Photos of Gokul Children's Hospital, Dhule – NICU, reception, consultation rooms and the Gokul Ayurveda & Lactation Clinic.", "gallery", body)


def build_contact():
    body = f"""
{page_hero([("Contact Us", "contact.html")], "Contact us", "Book an appointment by visiting or calling us!", "We are open 24/7 for emergencies. OPD consultations: " + S['hours_opd'] + ".", buttons=False)}
<section class="section-tight">
  <div class="container">{contact_tiles()}</div>
</section>
<section class="section-tight" id="book">
  <div class="container split" style="align-items:stretch">
    <div class="card" style="padding:clamp(22px,4vw,40px)">
      <p class="eyebrow">Get in touch</p>
      <h2>Request an appointment</h2>
      <p class="muted">We offer in-person visits and virtual consultations through video and audio calls. Send your request on WhatsApp or by email and our team will get back to you.</p>
      {booking_form("c", email_option=True, include_subject=True)}
    </div>
    <div style="display:grid;gap:16px;grid-template-rows:1fr auto">
      <iframe class="map" src="{S['map_embed']}" title="Map showing Gokul Children's Hospital, Malegaon Road, Dhule" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      <div class="card">
        <h3>{icon('map-pin')} Hospital address</h3>
        <p style="margin-bottom:14px">{S['address_1']},<br>{S['address_2']}</p>
        <p class="muted" style="margin-bottom:16px">Email: <a href="mailto:{S['email']}">{S['email']}</a>, <a href="mailto:{S['email_2']}">{S['email_2']}</a></p>
        <div class="btn-row"><a class="btn btn-teal btn-sm" href="{S['maps']}" target="_blank" rel="noopener">{icon('navigation')}Get directions</a><a class="btn btn-ghost btn-sm" href="{TEL}">{icon('phone')}{S['phone_display']}</a></div>
      </div>
    </div>
  </div>
</section>
"""
    page("contact.html", "Contact Us",
         "Contact Gokul Children's Hospital, Opposite Bank of Baroda, Malegaon Road, Dhule 424001. Call 095793 12398, WhatsApp, or email to book an appointment. Open 24/7.",
         "contact", body)


if __name__ == "__main__":
    build_home()
    build_about()
    build_services()
    build_facilities()
    build_clinics()
    build_gallery()
    build_contact()
