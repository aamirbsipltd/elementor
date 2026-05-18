#!/usr/bin/env python3
"""
Generate Elementor JSON page templates from a single Python config.

Each page is built as:
  1. HERO section — native Elementor widgets (Heading + Text + 2 Buttons + Image)
     Editable visually in Elementor's UI.
  2. BODY HTML widget — Custom HTML widget(s) reusing CSS from the Gutenberg
     ciwa-final build for sections too complex for free-Elementor widgets
     (card grids, tab toggles, accordion FAQs, contact forms).

Run:  python tools/build-templates.py
Output: templates/elementor/<slug>.json  (one per page)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "templates", "elementor")
os.makedirs(OUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Reusable section builders
# ---------------------------------------------------------------------------

def hero(slug, title, body, image, cta1=("LEARN MORE", "#"), cta2=("GET INVOLVED", "/volunteer-with-us/")):
    """Standard pink hero: 50/50 title+body+CTAs / image."""
    return {
        "id": f"{slug}_hero",
        "elType": "section",
        "settings": {
            "structure": "20",
            "background_background": "classic",
            "background_color": "#fce7f0",
            "padding": {"unit":"px","top":"80","right":"32","bottom":"96","left":"32","isLinked":False},
            "content_width": {"unit":"px","size":1320},
            "gap": "extended",
        },
        "elements": [
            {
                "id": f"{slug}_hero_c1",
                "elType": "column",
                "settings": {"_column_size": 50, "content_position": "center"},
                "elements": [
                    {
                        "id": f"{slug}_hero_h",
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": title,
                            "header_size": "h1",
                            "title_color": "#6a1753",
                            "typography_typography": "custom",
                            "typography_font_family": "Cormorant Garamond",
                            "typography_font_size": {"unit":"px","size":56},
                            "typography_font_weight": "400",
                            "typography_letter_spacing": {"unit":"px","size":-1.2},
                            "typography_line_height": {"unit":"em","size":1.0},
                            "typography_text_transform": "uppercase",
                        },
                    },
                    {
                        "id": f"{slug}_hero_b",
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": f"<p>{body}</p>",
                            "text_color": "#1a1a1a",
                            "typography_typography": "custom",
                            "typography_font_family": "Inter",
                            "typography_font_size": {"unit":"px","size":17},
                            "typography_line_height": {"unit":"em","size":1.6},
                            "_margin": {"unit":"px","top":"20","right":"0","bottom":"28","left":"0","isLinked":False},
                        },
                    },
                    {
                        "id": f"{slug}_hero_btn_html",
                        "elType": "widget",
                        "widgetType": "html",
                        "settings": {
                            "html": (
                                "<style>.ciwa-h-cta-wrap{display:flex;gap:14px;flex-wrap:wrap}"
                                ".ciwa-h-cta{background:#f68b3c;color:#fff;padding:13px 24px;border-radius:8px;font-family:'Cormorant Garamond',serif;font-size:14px;text-transform:uppercase;letter-spacing:1.5px;text-decoration:none;display:inline-block}"
                                ".ciwa-h-cta:hover{background:#e07d2e;color:#fff}"
                                ".ciwa-h-cta.outline{background:transparent;color:#6a1753;border:2px solid #6a1753;padding:11px 22px}"
                                "</style>"
                                f'<div class="ciwa-h-cta-wrap">'
                                f'<a class="ciwa-h-cta" href="{cta1[1]}">{cta1[0]} &rsaquo;</a>'
                                f'<a class="ciwa-h-cta outline" href="{cta2[1]}">{cta2[0]} &rsaquo;</a>'
                                f'</div>'
                            ),
                        },
                    },
                ],
            },
            {
                "id": f"{slug}_hero_c2",
                "elType": "column",
                "settings": {"_column_size": 50, "content_position": "center"},
                "elements": [
                    {
                        "id": f"{slug}_hero_img",
                        "elType": "widget",
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "{ASSETS}/" + image, "id": ""},
                            "image_size": "full",
                            "align": "center",
                            "border_radius": {"unit":"px","top":"18","right":"18","bottom":"18","left":"18","isLinked":True},
                        },
                    }
                ],
            },
        ],
    }


def html_section(slug, suffix, html, bg="#ffffff", padding=("80","32","80","32")):
    """Generic single-column section with one Custom HTML widget."""
    return {
        "id": f"{slug}_{suffix}",
        "elType": "section",
        "settings": {
            "background_background": "classic",
            "background_color": bg,
            "padding": {"unit":"px","top":padding[0],"right":padding[1],"bottom":padding[2],"left":padding[3],"isLinked":False},
            "content_width": {"unit":"px","size":1320},
        },
        "elements": [
            {
                "id": f"{slug}_{suffix}_c",
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": f"{slug}_{suffix}_h",
                        "elType": "widget",
                        "widgetType": "html",
                        "settings": {"html": html},
                    }
                ],
            }
        ],
    }


# ---------------------------------------------------------------------------
# Shared CSS prelude (included in every body HTML widget)
# Keeps widgets self-contained — each can be moved between pages safely.
# ---------------------------------------------------------------------------

SHARED_CSS = """
<style>
.ciwa-c, .ciwa-c * { box-sizing: border-box; font-family: 'Inter', sans-serif; }
.ciwa-c { color: #1a1a1a; line-height: 1.55; }
.ciwa-c h2, .ciwa-c h3, .ciwa-c h4 { font-family: 'Cormorant Garamond', serif; font-weight: 400; margin: 0; letter-spacing: 0.02em; }
.ciwa-c h2 { font-size: 44px; color: #6a1753; text-transform: uppercase; letter-spacing: -1px; }
.ciwa-c .pink { color: #ff6e6e; }
.ciwa-c .center { text-align: center; }
.ciwa-c .wrap-1320 { max-width: 1320px; margin: 0 auto; }
.ciwa-c .wrap-1100 { max-width: 1100px; margin: 0 auto; }
.ciwa-c .wrap-880 { max-width: 880px; margin: 0 auto; }
.ciwa-c .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.ciwa-c .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.ciwa-c .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.ciwa-c .card { background:#fff; border:1px solid #e6dce4; border-radius:14px; padding:24px; box-shadow:0 2px 6px rgba(0,0,0,.04); display:flex; flex-direction:column; gap:10px; }
.ciwa-c .card.purple { border-left:6px solid #6a1753; }
.ciwa-c .card.pink   { border-left:6px solid #e22371; }
.ciwa-c .card.orange { border-left:6px solid #f68b3c; }
.ciwa-c .card.coral  { border-left:6px solid #ff6e6e; }
.ciwa-c .card.teal   { border-left:6px solid #5bbdad; }
.ciwa-c .card.olive  { border-left:6px solid #aaa835; }
.ciwa-c .card h3 { font-size: 22px; }
.ciwa-c .card.purple h3 { color:#6a1753; }
.ciwa-c .card.pink h3   { color:#e22371; }
.ciwa-c .card.orange h3 { color:#f68b3c; }
.ciwa-c .card.coral h3  { color:#ff6e6e; }
.ciwa-c .card.teal h3   { color:#5bbdad; }
.ciwa-c .card p { margin: 0; font-size: 15px; color: #4a4a4a; line-height: 1.6; }
.ciwa-c .lead { font-size: 17px; color: #4a4a4a; line-height: 1.6; margin: 16px auto 48px; }
.ciwa-c .btn { background:#6a1753; color:#fff; padding:13px 26px; border-radius:8px; font-family:'Cormorant Garamond',serif; font-size:14px; text-transform:uppercase; letter-spacing:1.5px; text-decoration:none; display:inline-block; }
.ciwa-c .btn.orange { background:#f68b3c; }
.ciwa-c .btn.outline { background:transparent; color:#6a1753; border:2px solid #6a1753; padding:11px 24px; }
.ciwa-c .btn-row { display:flex; gap:14px; flex-wrap:wrap; justify-content:center; margin:32px 0 0; }
.ciwa-c .team-grid { display:grid; grid-template-columns:repeat(4, 1fr); gap:24px; max-width:1320px; margin:0 auto; }
.ciwa-c .team-card { background:#fff; border:1px solid #e6dce4; border-radius:14px; padding:24px 20px; text-align:center; display:flex; flex-direction:column; align-items:center; gap:8px; box-shadow:0 2px 6px rgba(0,0,0,.04); }
.ciwa-c .team-card img { width:96px; height:96px; border-radius:50%; object-fit:cover; background:#f3e7ee; }
.ciwa-c .team-card h4 { font-family:'Cormorant Garamond',serif; font-size:17px; font-weight:400; margin:4px 0 0; color:#1a1a1a; }
.ciwa-c .team-card .role { font-size:13px; color:#6a1753; margin:0; }
.ciwa-c .team-card .email a { font-size:12px; color:#e22371; text-decoration:none; word-break:break-all; }
.ciwa-c .stat-cards { display:grid; grid-template-columns:repeat(2, 1fr); gap:18px; max-width:743px; }
.ciwa-c .stat { background:#fff; border:1.5px solid #ccc; border-radius:14px; padding:28px 24px; }
.ciwa-c .stat.pink   { border-color:#e22371; } .ciwa-c .stat.pink .v   { color:#e22371; }
.ciwa-c .stat.dark   { border-color:#1a1a1a; } .ciwa-c .stat.dark .v   { color:#1a1a1a; }
.ciwa-c .stat.orange { border-color:#f69538; } .ciwa-c .stat.orange .v { color:#f69538; }
.ciwa-c .stat.coral  { border-color:#ff6e6e; } .ciwa-c .stat.coral .v  { color:#ff6e6e; }
.ciwa-c .stat .v { font-family:'Cormorant Garamond',serif; font-size:40px; line-height:1; margin-bottom:10px; }
.ciwa-c .stat .t { font-weight:600; font-size:16px; margin-bottom:8px; }
.ciwa-c .stat .b { color:#5b5b66; font-size:14px; }
.ciwa-c .form-row { display:flex; gap:22px; margin-bottom:22px; flex-wrap:wrap; }
.ciwa-c .form-row label { flex:1 1 calc(50% - 11px); display:flex; flex-direction:column; gap:8px; min-width:220px; }
.ciwa-c .form-row label.full { flex:1 1 100%; }
.ciwa-c .form-row label span { font-family:'Cormorant Garamond',serif; font-size:13px; letter-spacing:1px; text-transform:uppercase; color:#6a1753; }
.ciwa-c .form-row input, .ciwa-c .form-row select, .ciwa-c .form-row textarea { background:#fff; border:1px solid #d6c8d4; border-radius:8px; padding:12px 14px; font-size:15px; font-family:inherit; width:100%; box-sizing:border-box; }
.ciwa-c .form-row textarea { min-height:140px; resize:vertical; }
.ciwa-c .form-submit { background:#6a1753; color:#fff; border:0; padding:14px 32px; border-radius:8px; font-family:'Cormorant Garamond',serif; font-size:14px; text-transform:uppercase; letter-spacing:1.5px; cursor:pointer; }
.ciwa-c .form { max-width:880px; margin:0 auto; }
.ciwa-c .spotlight { background:#6a1753; color:#fff; text-align:center; padding:80px 32px; border-radius:0; margin:0 -32px; }
.ciwa-c .spotlight h2 { color:#fff; }
.ciwa-c .spotlight p { color:rgba(255,255,255,.9); margin:14px 0 28px; }
@media (max-width: 900px) {
  .ciwa-c .grid-2, .ciwa-c .grid-3, .ciwa-c .grid-4, .ciwa-c .team-grid, .ciwa-c .stat-cards { grid-template-columns: 1fr; }
}
</style>
"""


# ---------------------------------------------------------------------------
# Page configurations
# ---------------------------------------------------------------------------

def page_who_we_are():
    history = [
        ("1980s", "Founding & Anchoring Beginnings — established 1982 as a registered charity supporting immigrant women and their families in Calgary."),
        ("1990s", "Building Roots & Foundations — first language and settlement programs scaled across Calgary partner sites."),
        ("2000s", "CIWA Program Expansion & Recognition — employment, family, and child-care services added; major literacy and impact awards received."),
        ("2010s", "Growing Impact in the Community — citywide partnerships and youth-focused programming launch."),
        ("2020s", "Expansion & National Voice — reaching newcomers across Alberta with virtual programming and a national voice on immigration policy."),
        ("2025",  "A Renewed Chapter — new leadership, expanded board, and a renewed strategic plan for the next decade."),
    ]
    facts = [
        ("pink",   "We offer over 50 programs and services for immigrant women and their families."),
        ("orange", "We host programs and services in over 90 community locations."),
        ("purple", "Clients fleeing family violence have access to emergency housing support."),
        ("coral",  "Childcare support is available for all clients attending CIWA services."),
        ("pink",   "Certified interpreters and translators offer services in 37 languages."),
        ("orange", "Over 230 businesses and employers collaborate with us to support employment access."),
    ]
    fact_html = "".join(f'<div class="card {c}"><p>{t}</p></div>' for c, t in facts)
    hist_html = "".join(f'<div class="card purple"><h3>{y}</h3><p>{t}</p></div>' for y, t in history)
    body_html = (
        SHARED_CSS
        + '<div class="ciwa-c">'
        + '<h2 class="center wrap-1100" style="margin-bottom:24px;">WHO WE <span class="pink">ARE</span></h2>'
        + '<p class="center lead wrap-1100">Canadian Immigrant Women\'s Association (CIWA) is a non-profit organization established in 1982 as a registered charity. CIWA is a culturally diverse settlement agency that recognizes the strengths and contributions of immigrant women.</p>'
        + '<h2 class="center" style="margin:48px 0 32px;">HISTORY</h2>'
        + f'<div class="wrap-1100" style="display:flex;flex-direction:column;gap:16px;">{hist_html}</div>'
        + '<div class="grid-3 wrap-1320" style="margin-top:64px;gap:24px;">'
        + '<div style="background:#6a1753;color:#fff;border-radius:14px;padding:36px 32px;"><h3 style="color:#fff;font-size:28px;">Vision</h3><p style="color:rgba(255,255,255,.95);margin-top:12px;">National leader in transitioning immigrant women to success in Canada.</p></div>'
        + '<div style="background:#f68b3c;color:#fff;border-radius:14px;padding:36px 32px;"><h3 style="color:#fff;font-size:28px;">Mission</h3><p style="color:rgba(255,255,255,.95);margin-top:12px;">Empower immigrant women. Enrich Canadian society.</p></div>'
        + '<div style="background:#e22371;color:#fff;border-radius:14px;padding:36px 32px;"><h3 style="color:#fff;font-size:28px;">Values</h3><p style="color:rgba(255,255,255,.95);margin-top:12px;">Equity. Excellence. Collaboration. Inclusiveness. Empowerment.</p></div>'
        + '</div>'
        + '<h2 class="center" style="margin:64px 0 32px;">QUICK <span class="pink">FACTS</span></h2>'
        + f'<div class="grid-3 wrap-1320">{fact_html}</div>'
        + '<div class="spotlight" style="margin-top:64px;"><h2>LAND <span style="color:#ff6e6e">ACKNOWLEDGEMENT</span></h2><p class="wrap-1100">As an immigrant-serving organization, we acknowledge that we work on the traditional lands of the Treaty 7 Nations: the Blackfoot Confederacy (Siksika, Piikani, Kainai), the Tsuut\'ina Nation, and the Stoney Nakoda Nations (Chiniki, Bearspaw, Goodstoney). We honour the diverse histories, languages, and cultures of the Indigenous peoples who have lived on this land for generations.</p></div>'
        + '</div>'
    )
    return [
        hero("wwa", "WHO WE ARE", "Canadian Immigrant Women's Association — a non-profit established in 1982 supporting immigrant and refugee women across Calgary.", "welcome/collage.png", cta1=("OUR HISTORY","#history")),
        html_section("wwa", "body", body_html, bg="#ffffff"),
    ]


def page_program(slug, title, intro, hero_img, programs_label, programs, gain, didyou_text, didyou_img):
    """5 program pages share this layout (settlement, employment, family, language, wellness)."""
    prog_html = "".join(
        f'<div class="card {p[0]}"><h3>{p[1]}</h3><p>{p[2]}</p></div>'
        for p in programs
    )
    gain_html = "".join(
        f'<div class="card {bg}" style="background:{bg_color};color:#fff;border:none;"><p style="color:#fff;font-family:\'Cormorant Garamond\',serif;font-size:16px;line-height:1.45;">{text}</p></div>'
        for bg, bg_color, text in gain
    )
    body_html = (
        SHARED_CSS
        + '<div class="ciwa-c">'
        + f'<h2 class="center" id="programs" style="margin-bottom:48px;">PROGRAMS UNDER <span class="pink">{programs_label}</span></h2>'
        + f'<div class="grid-2 wrap-1320" style="margin-bottom:48px;">{prog_html}</div>'
        + '<h2 class="center" style="margin:64px 0 32px;">WHAT YOU <span class="pink">GAIN</span></h2>'
        + f'<div class="grid-4 wrap-1320">{gain_html}</div>'
        + '<h2 class="center" style="margin:64px 0 24px;">DID YOU <span class="pink">KNOW?</span></h2>'
        + f'<p class="center lead wrap-1100" style="font-style:italic;">"{didyou_text}"</p>'
        + f'<img src="{{ASSETS}}/{didyou_img}" alt="" style="display:block;max-width:880px;margin:0 auto 64px;width:100%;height:auto;border-radius:14px;">'
        + '</div>'
    )
    return [
        hero(slug, title, intro, hero_img),
        html_section(slug, "body", body_html, bg="#ffffff"),
    ]


def page_team(slug, title, intro, hero_img, h2_first, h2_second, team_members, has_email=True, sub_text=None, quote=None):
    """Leadership / Board / Volunteer-spotlights: 12-person grid."""
    cards = []
    for p in team_members:
        email_html = f'<p class="email"><a href="mailto:{p["email"]}">{p["email"]}</a></p>' if has_email and p.get("email") else ""
        cards.append(
            f'<div class="team-card"><img src="{{ASSETS}}/voices/avatar.svg" alt=""><h4>{p["name"]}</h4><p class="role">{p["role"]}</p>{email_html}</div>'
        )
    team_html = "".join(cards)
    sub_html = f'<p class="center wrap-1100" style="font-weight:600;margin-bottom:16px;text-transform:uppercase;letter-spacing:.4px;">{sub_text}</p>' if sub_text else ""
    quote_html = f'<div style="background:#f6eef4;padding:32px 40px;border-radius:14px;max-width:1100px;margin:48px auto 0;"><p style="font-family:\'Cormorant Garamond\',serif;font-size:18px;font-style:italic;color:#6a1753;text-align:center;">{quote}</p></div>' if quote else ""
    body_html = (
        SHARED_CSS
        + '<div class="ciwa-c">'
        + f'<h2 class="center" style="margin-bottom:16px;">{h2_first} <span class="pink">{h2_second}</span></h2>'
        + sub_html
        + f'<p class="center lead wrap-1100">{intro}</p>'
        + f'<div class="team-grid">{team_html}</div>'
        + quote_html
        + '</div>'
    )
    return [
        hero(slug, title, intro, hero_img),
        html_section(slug, "body", body_html, bg="#ffffff"),
    ]


def page_list(slug, title, intro, hero_img, h2_first, h2_second, items, item_class="card purple"):
    """Awards / Useful Links / etc. — long list of items."""
    items_html = ""
    if isinstance(items[0], tuple) and len(items[0]) == 2 and items[0][0] and items[0][0][0].isdigit():
        # Year-grouped (awards): [(year, text), ...]
        current_year = None
        for y, t in items:
            if y != current_year:
                if current_year is not None:
                    items_html += '</div>'
                items_html += f'<h3 style="font-family:\'Cormorant Garamond\',serif;font-size:26px;color:#e22371;margin:32px 0 12px;border-bottom:2px solid #e6dce4;padding-bottom:8px;">{y}</h3><div style="display:flex;flex-direction:column;gap:8px;">'
                current_year = y
            items_html += f'<p class="card purple" style="margin:0;font-size:15px;line-height:1.55;">{t}</p>'
        if current_year is not None:
            items_html += '</div>'
    else:
        # Plain list of (label, url) tuples
        items_html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:32px 48px;max-width:1320px;margin:0 auto;">'
        mid = (len(items) + 1) // 2
        for col in (items[:mid], items[mid:]):
            items_html += '<ul style="list-style:none;padding:0;margin:0;">'
            for lbl, url in col:
                items_html += f'<li style="border-bottom:1px solid #e6dce4;padding:14px 0;"><a href="{url}" style="color:#1a1a1a;text-decoration:none;display:flex;justify-content:space-between;">{lbl} &rsaquo;</a></li>'
            items_html += '</ul>'
        items_html += '</div>'

    body_html = (
        SHARED_CSS
        + '<div class="ciwa-c">'
        + f'<h2 class="center" style="margin-bottom:24px;">{h2_first} <span class="pink">{h2_second}</span></h2>'
        + f'<p class="center lead wrap-1100">{intro}</p>'
        + f'<div class="wrap-1100">{items_html}</div>'
        + '</div>'
    )
    return [
        hero(slug, title, intro, hero_img),
        html_section(slug, "body", body_html, bg="#ffffff"),
    ]


# ---------------------------------------------------------------------------
# Page registry — defines what each page contains
# ---------------------------------------------------------------------------

PAGES = {
    "home": {
        "title": "Home",
        "build": lambda: [
            hero("home", "EMPOWERING IMMIGRANT WOMEN", "For over 40 years CIWA has empowered immigrant and refugee women to build successful lives in Calgary through settlement, employment, language, and family programs.", "welcome/collage.png", cta1=("EXPLORE PROGRAMS","#programs"), cta2=("DONATE NOW","/donate/")),
            html_section("home", "body", SHARED_CSS + '<div class="ciwa-c"><h2 class="center" id="programs">PROGRAMS & SERVICES <span class="pink">THAT EMPOWER WOMEN</span></h2><p class="center lead wrap-1100">CIWA offers a wide range of programs designed to help immigrant and refugee women build confidence, develop skills, and thrive in Canada.</p><div class="grid-3 wrap-1320" style="margin-bottom:48px;"><div class="card purple"><h3>SETTLEMENT SUPPORT</h3><p>Starting a new life in Canada can feel overwhelming. Our settlement services provide guidance, resources, and community connections.</p></div><div class="card pink"><h3>EMPLOYMENT & TRAINING</h3><p>Build the skills you need to succeed in the Canadian workforce. Job-ready training, mentors, and employer partners.</p></div><div class="card orange"><h3>FAMILY SERVICES</h3><p>Support for families is essential to building strong communities. Childcare, parenting, and life-in-Canada navigation.</p></div><div class="card coral"><h3>LANGUAGE TRAINING</h3><p>Improve your English communication skills with childcare included so you can attend without missing a thing.</p></div><div class="card olive"><h3>WELLBEING & RESILIENCY</h3><p>Counselling, peer support, and group programs that help women navigate stress, isolation, and starting over.</p></div><div class="card teal"><h3>SMILES CHILDCARE</h3><p>Our social-enterprise childcare centre in downtown Calgary where your child feels safe, supported, and happy.</p></div></div><div class="spotlight"><h2>OUR IMPACT</h2><p class="wrap-880">For over 40 years CIWA has supported immigrant and refugee women through programs that promote independence, leadership, and community connection.</p><div class="btn-row"><a class="btn orange" href="/annual-reports/">SEE OUR ANNUAL REPORTS &rsaquo;</a></div></div></div>', bg="#fdf6ef"),
        ],
    },
    "who-we-are": {"title": "Who We Are", "build": page_who_we_are},
    "leadership-governance": {
        "title": "Leadership & Governance",
        "build": lambda: page_team(
            "lead",
            "LEADERSHIP & GOVERNANCE",
            "Meet the leadership team driving CIWA's programs, partnerships, and community impact.",
            "welcome/collage.png",
            "LEADERSHIP &", "GOVERNANCE",
            [
                {"name":"Paula Calderon","role":"Chief Executive Officer","email":"ceo@ciwa.org"},
                {"name":"Biraj Patel","role":"Chief Financial Officer","email":"cfo@ciwa.org"},
                {"name":"Eva Szasz-Redmond","role":"Chief Operating Officer","email":"coo@ciwa.org"},
                {"name":"Nurishah Dharamsi","role":"Director Communications & Partnerships","email":"media@ciwa.org"},
                {"name":"Leanna Kielau","role":"Director People & Culture","email":"dhra@ciwa.org"},
                {"name":"Penny Bates","role":"Director SMILES Childcare","email":"info@smileschildcarecentre.ca"},
                {"name":"Veronica Aliu","role":"Family Services Manager","email":"familyservices@ciwa.org"},
                {"name":"Gurpreet Kaur","role":"Language Training & Childcare Manager","email":"language@ciwa.org"},
                {"name":"Kemi Awodein","role":"Settlement & Integration Manager","email":"settlement@ciwa.org"},
                {"name":"Sarah Williams","role":"Employment Manager","email":"employment@ciwa.org"},
                {"name":"Priya Sharma","role":"Wellbeing & Resiliency Manager","email":"wellbeing@ciwa.org"},
                {"name":"Amina Okonkwo","role":"Programs & Partnerships Coordinator","email":"programs@ciwa.org"},
            ],
        ),
    },
    "board-of-directors": {
        "title": "Board of Directors",
        "build": lambda: page_team(
            "board",
            "BOARD OF DIRECTORS",
            "The CIWA Board of Directors brings together community, business, and governance leaders dedicated to advancing the mission of empowering immigrant women.",
            "instagram/ig3.png",
            "BOARD OF", "DIRECTORS",
            [
                {"name":"Jung Lee","role":"Board Chair"},
                {"name":"Jennifer McFadyen","role":"Vice-Chair"},
                {"name":"Tony DiMaio","role":"Treasurer"},
                {"name":"Hajar Kacem","role":"Governance Committee Chair"},
                {"name":"Teisha Iglesias","role":"HR Committee Chair"},
                {"name":"Jeni Piepgrass","role":"Director"},
                {"name":"Bernadette Charan","role":"Director"},
                {"name":"KayLynn Litton","role":"Director"},
                {"name":"Dani Grover","role":"Director"},
                {"name":"Yewande Esan","role":"Director"},
                {"name":"Alishah Janmohamed","role":"Director"},
                {"name":"Raisa Chowdhury","role":"Director"},
            ],
            has_email=False,
            sub_text="BOARD OF DIRECTORS 2023-2026",
            quote='"CIWA demonstrates superior relationship building initiatives, such as this retreat, which is relevant today and engaging with members, staff, and the community."',
        ),
    },
    "awards-recognition": {
        "title": "Awards & Recognition",
        "build": lambda: page_list(
            "awards",
            "AWARDS & RECOGNITION",
            "Decades of recognition for CIWA's impact on immigrant women and their families across Calgary and Canada.",
            "welcome/collage.png",
            "AWARDS &", "RECOGNITION",
            [
                ("2025","Outstanding Nonprofit Agency Award at the South Asian Inspiration Awards"),
                ("2025","Inclusive Organization Award by Immigrant Champions of Canada (ICC)"),
                ("2025","Canada Life Literacy Innovation Award presented by ABC Life Literacy Canada"),
                ("2024","Appreciation Award presented by MD International"),
                ("2024","Alberta Immigrant Impact Award — Newcomer Champion Award presented to Paula Calderon"),
                ("2023","United Way Calgary Bhayana Awards presented to Azita Afsharnejat"),
                ("2023","Because Mothers Matter Awards presented to Luz Buritica, HIPPY Program Coordinator"),
                ("2021","Girls at Bat All-Star Coach Award by Jays Care Foundation"),
                ("2020","Canada's Most Powerful CEOs presented to Beba Svigir by KPMG"),
                ("2018","Making a Difference for Women Award presented to Beba Svigir by Soroptimist International of Calgary"),
                ("2018","Leaders in Diversity Award presented to CIWA by FACL Western"),
                ("2017","Innovation Award presented by The Great-West Life, London Life and Canada Life Literacy"),
                ("2016","Life of Learning Award (LOLA) — Learning Champion category presented to CIWA"),
                ("2014","Council of the Federation Literacy Award for Alberta presented to CIWA"),
                ("2013","Calgary Herald Christmas Fund presented to CIWA"),
                ("2010","Canada's Citizenship Award presented to Shokoofeh Moussavi"),
            ],
        ),
    },
    "annual-reports": {
        "title": "Annual Reports",
        "build": lambda: [
            hero("ar", "ANNUAL REPORTS", "Explore our annual reports to see how we are creating impact, empowering communities, and driving meaningful change.", "events/e2.png"),
            html_section("ar", "body", SHARED_CSS + '<div class="ciwa-c"><h2 class="center">ANNUAL <span class="pink">REPORTS</span></h2><p class="center lead wrap-1100">Our annual reports provide a comprehensive overview of our programs, impact, and financial performance.</p><h3 class="center" style="color:#e22371;font-size:24px;margin-bottom:48px;text-transform:uppercase;letter-spacing:.04em;">TRANSPARENCY & ACCOUNTABILITY</h3>' + '<div class="grid-3 wrap-1320">' + ''.join(f'<div class="card" style="border-top:6px solid #6a1753;"><h3 style="color:#6a1753;">{y} ANNUAL REPORT</h3><p>A year of growth, resilience, and community impact.</p><h4 style="font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:.04em;margin-top:8px;">Highlights:</h4><ul style="margin:0;padding-left:18px;font-size:14px;color:#4a4a4a;line-height:1.55;"><li>10,000+ women supported</li><li>Expanded employment programs</li><li>New community partnerships</li></ul><div style="display:flex;gap:10px;margin-top:auto;padding-top:12px;flex-wrap:wrap;"><a class="btn" href="#report">View Report</a><a class="btn outline" href="#download">Download PDF</a></div></div>' for y in ("2025","2024","2023")) + '</div><div class="btn-row" style="margin-top:48px;"><a class="btn orange" href="#all">EXPLORE ALL ANNUAL REPORTS &rsaquo;</a></div></div>', bg="#ffffff"),
        ],
    },
    "settlement-supports": {
        "title": "Settlement Supports",
        "build": lambda: page_program(
            "set", "SETTLEMENT SUPPORTS",
            "Help new arrivals find footing fast — housing, ID, schools, healthcare, and a guided path through the first months in Canada.",
            "welcome/collage.png", "SETTLEMENT SUPPORT",
            [
                ("purple", "Settlement and Referral", "Document help (SIN, AHC, ID), and warm referrals to housing, banking, schools, and healthcare partners."),
                ("pink",   "Case Management Support", "Personalized case plan, regular check-ins, and coordinated handoffs across CIWA programs."),
                ("orange", "Community Connections", "Group sessions, peer mentors, and partner events that build social belonging."),
                ("coral",  "Youth Support", "School advocacy, after-school mentorship, and identity-building groups for immigrant youth."),
            ],
            [
                ("pink","#e22371","A clear first-90-days plan to get oriented in Calgary."),
                ("orange","#f68b3c","Trusted referrals across 230+ employer and community partners."),
                ("purple","#6a1753","Bilingual support in 37+ languages from certified staff."),
                ("coral","#ff6e6e","Childcare and family support while you attend services."),
            ],
            "Thousands of immigrant women navigate their first year in Canada with the help of a CIWA settlement counsellor.",
            "welcome/collage.png",
        ),
    },
    "employment-skills-training": {
        "title": "Employment Skills & Training",
        "build": lambda: page_program(
            "emp", "EMPLOYMENT SKILLS & TRAINING",
            "Job-readiness training, sector-specific certifications, and one-on-one career coaching that turns Canadian work experience into long-term careers.",
            "instagram/ig2.png", "SKILLS & TRAINING",
            [
                ("purple", "Job-Readiness Programs", "Resume, interview, and Canadian workplace culture training — 4-week intake every month."),
                ("pink",   "Career Counselling", "One-on-one career counsellors who match skills and goals to Canadian opportunities."),
                ("orange", "Employment Skills Training", "Hands-on certifications: customer service, hospitality, security, food service, accounting, IT."),
                ("coral",  "Career-Building Coaching", "Post-placement coaching and employer-side advocacy to make first jobs become careers."),
            ],
            [
                ("pink","#e22371","Job placement support with 230+ partner employers."),
                ("orange","#f68b3c","Free certifications in 7+ sectors."),
                ("purple","#6a1753","Childcare while you train — included."),
                ("coral","#ff6e6e","Up to 90 days of post-placement mentorship."),
            ],
            "71% of participants find employment within 6 months of completing a CIWA training program.",
            "instagram/ig3.png",
        ),
    },
    "family-parenting-supports": {
        "title": "Family & Parenting Supports",
        "build": lambda: page_program(
            "fam", "FAMILY & PARENTING SUPPORTS",
            "Parenting, family violence support, and child-development programs that strengthen immigrant families across every life stage.",
            "voices/photo-1.png", "FAMILY & PARENTING SUPPORT",
            [
                ("purple", "Parenting Education", "Group workshops on Canadian parenting norms, child development, communication, and culture at home."),
                ("pink",   "Child & Youth Programs", "Homework clubs, summer camps, and identity-building groups for newcomer children ages 6–18."),
                ("orange", "Family Counselling", "Confidential family counselling — couples, parents, and individuals — in 37+ languages."),
                ("coral",  "Childcare On Site", "Drop-in childcare available while you attend CIWA programs, language classes, or counselling."),
            ],
            [
                ("pink","#e22371","A safe space to navigate parenting in a new culture."),
                ("orange","#f68b3c","Confidential, multilingual counselling support."),
                ("purple","#6a1753","On-site childcare while you attend services."),
                ("coral","#ff6e6e","Programs for the whole family across age groups."),
            ],
            "Thousands of families supported every year — across more than 90 community locations in Calgary.",
            "voices/photo-2.png",
        ),
    },
    "language-training": {
        "title": "Language Training",
        "build": lambda: page_program(
            "lang", "LANGUAGE TRAINING",
            "CLB-aligned English instruction at every level — combined with childcare so women can attend without missing a thing.",
            "instagram/ig1.png", "LANGUAGE TRAINING",
            [
                ("purple", "English Language Classes", "CLB 1–8 daytime classes — reading, writing, listening, speaking. Small groups, certified instructors."),
                ("pink",   "Workplace Language Training", "Sector-specific English for healthcare, hospitality, retail, and customer service."),
                ("orange", "Conversation Circles", "Drop-in conversation groups for confidence-building, pronunciation, and community connections."),
                ("coral",  "Literacy & Foundations", "Foundational English literacy for women with low or no prior schooling."),
            ],
            [
                ("pink","#e22371","CLB-aligned curriculum that fits any starting level."),
                ("orange","#f68b3c","Childcare during every class — included."),
                ("purple","#6a1753","Job-ready language skills for Canadian workplaces."),
                ("coral","#ff6e6e","Free, accessible, and welcoming to all backgrounds."),
            ],
            "Thousands of women improve their English skills each year through CIWA classes.",
            "instagram/ig4.png",
        ),
    },
    "language-training-2": {
        "title": "Wellness Programs",
        "build": lambda: page_program(
            "well", "MENTAL HEALTH AND WELLBEING",
            "Counselling, peer support, and group programs that help immigrant women navigate stress, isolation, and the emotional weight of starting over.",
            "voices/photo-2.png", "HEALTH & WELLBEING",
            [
                ("purple", "Counselling & Emotional Support", "One-on-one trauma-informed counselling in 37+ languages — confidential and free."),
                ("pink",   "Wellness Workshops", "Group workshops on stress, sleep, parenting, and managing the emotional load of resettlement."),
                ("orange", "Peer Support Groups", "Facilitated peer support groups where women share lived experience and build belonging."),
                ("coral",  "Crisis & Referral", "Immediate-need triage and warm referrals to specialized mental health supports."),
            ],
            [
                ("pink","#e22371","A safe, confidential space to be heard."),
                ("orange","#f68b3c","Counselling and groups in 37+ languages."),
                ("purple","#6a1753","Childcare available while you attend."),
                ("coral","#ff6e6e","Connections to specialized supports when needed."),
            ],
            "Thousands of women access support programs every year — confidential, multilingual, and free.",
            "voices/photo-1.png",
        ),
    },
    "donate": {
        "title": "Donate",
        "build": lambda: [
            hero("don", "INVEST IN HER POTENTIAL, TRANSFORM A COMMUNITY", "Your gift powers settlement, skills training, and mentorship — measurable change in the lives of women and families across Calgary.", "instagram/ig5.png", cta1=("DONATE NOW","#donate-form")),
            html_section("don", "body",
                SHARED_CSS + '<div class="ciwa-c"><p class="center" style="color:#e22371;font-size:13px;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">WHERE DONATIONS GO</p><h2 class="center">MEASURABLE IMPACT, <span class="pink">REAL LIVES</span></h2><div class="grid-3 wrap-1320" style="margin:48px 0;">'
                + '<div class="stat pink"><div class="v">2,400+</div><div class="t">Skills Training</div><div class="b">Direct impact on employment readiness through technical and vocational programs.</div></div>'
                + '<div class="stat orange"><div class="v">1,100+</div><div class="t">Career Support</div><div class="b">Job placement assistance and one-on-one mentorship for lasting career growth.</div></div>'
                + '<div class="stat coral"><div class="v">8,500+</div><div class="t">Community Impact</div><div class="b">Women supported annually across 12 regions, creating stronger local economies.</div></div>'
                + '</div><div class="spotlight" style="margin:64px -32px;"><p class="wrap-1080" style="font-family:\'Cormorant Garamond\',serif;font-size:22px;line-height:1.5;font-style:italic;">"When I donated $100, I didn\'t expect to receive a letter six months later from Amara — a young woman in Nairobi who\'d completed her coding bootcamp and landed her first job. That\'s when I knew every dollar counted."</p><p style="color:rgba(255,255,255,.85);font-size:14px;">— Sarah M., Monthly Donor since 2022</p></div>'
                + '<h2 class="center" id="donate-form" style="margin:64px 0 32px;">MAKE YOUR GIFT <span class="pink">TODAY</span></h2><p class="center lead wrap-880">Choose an amount that works for you. Every gift changes a life.</p>'
                + '<form class="form" action="#" method="post" style="background:#fff;padding:32px;border-radius:14px;box-shadow:0 2px 8px rgba(0,0,0,.05);"><div class="form-row" style="margin-bottom:14px;">'
                + ''.join(f'<label style="flex:1 1 calc(50% - 11px);"><span>${amt}</span><input type="radio" name="gift" value="{amt}"></label>' for amt in ("25","50","100","250"))
                + '</div><div class="form-row"><label class="full"><span>Custom amount:</span><input type="number" name="custom_amount" placeholder="$"></label></div><div class="form-row"><label class="full"><span>First Name:</span><input type="text" name="first_name"></label></div><div class="form-row"><label class="full"><span>Email:</span><input type="email" name="email"></label></div><div class="form-row"><label class="full"><span>Message:</span><textarea name="message" rows="4"></textarea></label></div><div style="display:flex;justify-content:flex-end;"><button type="submit" class="form-submit">COMPLETE DONATION</button></div></form></div>',
                bg="#fdf6ef",
            ),
        ],
    },
    "volunteer-with-us": {
        "title": "Volunteer With Us",
        "build": lambda: [
            hero("vol", "VOLUNTEER WITH US", "Be a force for community. Volunteer alongside immigrant women across settlement, employment, childcare, and youth programs.", "contact/group.png"),
            html_section("vol", "body",
                SHARED_CSS + '<div class="ciwa-c"><h2 class="center">VOLUNTEER WITH <span class="pink">US</span></h2><p class="center lead wrap-1100">CIWA volunteers play a critical role in the success of programs and services for immigrant women and their families. Whether you bring an hour a week or a whole season, your time changes lives.</p><h3 class="center" style="color:#6a1753;font-size:30px;margin-bottom:32px;">OPPORTUNITIES</h3>'
                + '<div class="wrap-1100" style="display:flex;flex-direction:column;gap:16px;">'
                + '<div class="card pink"><h3>English as a Second Language (ESL) Tutor</h3><p>Help build conversational and workplace English skills with women in CIWA programs. Online and in-person formats available.</p><a class="btn" href="#volunteer-contact" style="align-self:flex-start;">Read More &rsaquo;</a></div>'
                + '<div class="card purple"><h3>Childcare Team Volunteer</h3><p>Assist in the care of children from 6 months to 8 years old while their mothers attend CIWA programs.</p><a class="btn" href="#volunteer-contact" style="align-self:flex-start;">Read More &rsaquo;</a></div>'
                + '<div class="card orange"><h3>Group Leader / Facilitator: Mental Health & Addictions Support</h3><p>Run group sessions on mental health and wellbeing. Training and supervision provided.</p><a class="btn" href="#volunteer-contact" style="align-self:flex-start;">Read More &rsaquo;</a></div>'
                + '<div class="card coral"><h3>Summer Camp Volunteer</h3><p>Support youth in our 6-week summer camp engaging 200+ children, ages 6–13.</p><a class="btn" href="#volunteer-contact" style="align-self:flex-start;">Read More &rsaquo;</a></div>'
                + '<div class="card teal"><h3>Youth Career Exploration Mentor</h3><p>Mentor CIWA youth with career exploration, skill-building, and personal development.</p><a class="btn" href="#volunteer-contact" style="align-self:flex-start;">Read More &rsaquo;</a></div>'
                + '</div></div>',
                bg="#ffffff",
            ),
        ],
    },
    "become-a-member": {
        "title": "Become a Member",
        "build": lambda: [
            hero("mem", "BECOME A MEMBER", "Join a community of women and allies advancing settlement, employment, and belonging across Calgary.", "instagram/ig4.png", cta1=("JOIN NOW","#tiers")),
            html_section("mem", "body",
                SHARED_CSS + '<div class="ciwa-c" id="tiers"><h2 class="center">BECOME A <span class="pink">MEMBER</span></h2><p class="center lead wrap-1100">CIWA memberships expire on March 31 annually. If you purchased your membership between January 1 and March 31 of the same year, your membership will be valid until March 31 of the following year.</p><p class="center" style="margin-bottom:40px;"><a href="#bylaws" style="color:#6a1753;text-decoration:underline;font-weight:600;">Click to download required document: Memberships Bylaws &rsaquo;</a></p>'
                + '<div class="wrap-1080" style="display:flex;flex-direction:column;gap:16px;">'
                + ''.join(
                    '<div class="card" style="padding:24px 28px;"><div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:16px;"><h3 style="margin:0;color:#1a1a1a;">' + t + '</h3><p style="margin:0;font-family:\'Cormorant Garamond\',serif;font-size:22px;color:#e22371;">$' + p + ' <span style="font-size:13px;color:#8a7a87;margin-left:8px;">No expiration</span></p></div><p>' + b + '</p><div style="margin-top:auto;"><a class="btn" href="#join">SELECT &rsaquo;</a></div></div>'
                    for t, p, b in (
                        ("Individual Voting Status (New Membership)", "10", "Purchase a new membership for individual voting status. Please specify number of years."),
                        ("Individual Voting Status (Renewal)", "10", "Renew your individual voting membership for one or more additional years."),
                        ("Organizational Membership (New)", "50", "Purchase a new organizational membership. Eligible for non-profits and community groups."),
                        ("Lifetime Membership", "100", "Become a lifetime member of CIWA and support our work for years to come."),
                    )
                )
                + '</div></div>',
                bg="#ffffff",
            ),
        ],
    },
    "news": {
        "title": "News",
        "build": lambda: [
            hero("news", "NEWS", "Stories, milestones, and updates from CIWA and the immigrant women we work alongside.", "events/e1.png"),
            html_section("news", "body",
                SHARED_CSS + '<div class="ciwa-c"><h2 class="center" style="margin-bottom:48px;">LATEST <span class="pink">NEWS</span></h2><div class="grid-2 wrap-1320">'
                + ''.join(
                    '<div class="card" style="padding:0;overflow:hidden;"><img src="{ASSETS}/' + img + '" alt="" style="width:100%;height:280px;object-fit:cover;display:block;"><div style="padding:24px;display:flex;flex-direction:column;gap:10px;"><h3 style="color:#1a1a1a;">' + t + '</h3><p style="color:#e22371;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin:0;">Dec 16, 2025</p><p>' + b + '</p><a href="#article" style="color:#6a1753;font-size:14px;text-transform:uppercase;letter-spacing:.04em;text-decoration:none;">Read More &rsaquo;</a></div></div>'
                    for img, t, b in (
                        ("events/e1.png", "Ron Ghitter CM Scholarship Fund Recipients 2025", "Celebrating 18 outstanding women who have been selected as this year's recipients. Each receives a $2,500 scholarship for education and career goals."),
                        ("news/n1.png", "CIWA is Turning a New Leaf", "Today we announce a major new chapter for CIWA — new programs, expanded reach, and a renewed commitment to immigrant women across Calgary and beyond."),
                        ("instagram/ig1.png", "Roli's Story", "Roli arrived in Calgary with two children and no English. Two years later she runs her own catering business — here's how CIWA programs helped."),
                        ("instagram/ig4.png", "Volunteers Spend an Hour Daily", "Our 140+ volunteers spend an average of one hour every day supporting newcomers — small interactions compound into lasting impact."),
                        ("events/e3.png", "Cecilia's Story", "Cecilia joined CIWA's bridge-to-work program in 2023. Today she's leading a team at a Calgary biotech firm — and mentoring the next cohort."),
                        ("news/n2.png", "More Scholarship Stories", "Read the full list of this year's Ron Ghitter CM Scholarship recipients and the inspiring journeys behind each award."),
                    )
                )
                + '</div></div>',
                bg="#ffffff",
            ),
        ],
    },
    "events": {
        "title": "Events",
        "build": lambda: [
            hero("ev", "EVENTS", "Workshops, training, and gatherings — open to CIWA participants and community members.", "events/e3.png", cta1=("SEE UPCOMING","#upcoming")),
            html_section("ev", "body",
                SHARED_CSS + '<div class="ciwa-c" id="upcoming"><h2 class="center" style="margin-bottom:32px;">UPCOMING <span class="pink">EVENTS</span></h2><div class="btn-row" style="margin-bottom:40px;"><a class="btn" href="#">All</a><a class="btn outline" href="#">Upcoming</a></div><div class="wrap-1100" style="display:flex;flex-direction:column;gap:24px;">'
                + ''.join(
                    '<div class="card" style="flex-direction:row;gap:20px;align-items:center;padding:20px;"><img src="{ASSETS}/' + img + '" alt="" style="width:30%;min-width:200px;height:160px;object-fit:cover;border-radius:10px;flex-shrink:0;"><div style="flex:1;"><p style="display:inline-block;padding:4px 12px;background:#fce7f0;color:#e22371;border-radius:999px;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin:0 0 8px;">' + d + '</p><h3 style="color:#1a1a1a;margin:0 0 8px;font-size:18px;">' + t + '</h3><p style="margin:0 0 10px;">' + b + '</p><a href="#register" style="color:#6a1753;text-decoration:none;font-size:13px;text-transform:uppercase;letter-spacing:.04em;">Read More &rsaquo;</a></div></div>'
                    for img, d, t, b in (
                        ("events/e1.png", "Feb 9, 2026", "HOSPITALITY TRAINING FOR IMMIGRANT WOMEN", "Hands-on hospitality training — front of house, food service, event support."),
                        ("events/e2.png", "Apr 13, 2026", "CUSTOMER SERVICE TRAINING", "Customer Service certification: service workflows, conflict de-escalation, CRM tools."),
                        ("events/e3.png", "May 7, 2026", "BRIDGING THE GAP FOR FOREIGN TRAINED ACCOUNTANTS", "8-week intensive bridging program — CPA prep, Canadian workplace integration."),
                        ("instagram/ig2.png", "Apr 20, 2026", "OFFICE SKILLS TRAINING FOR STEM PROFESSIONALS", "Office skills and professional Canadian workplace English for women with STEM backgrounds."),
                        ("instagram/ig5.png", "Apr 20, 2026", "CULINARY SKILLS TRAINING", "Free intensive culinary training — kitchen safety, station prep, customer service."),
                        ("news/n1.png", "Apr 27, 2026", "SECURITY GUARD TRAINING", "Alberta Security Guard licensing prep, on-the-job placement, CPR / First Aid included."),
                    )
                )
                + '</div><div class="btn-row" style="margin-top:48px;"><a class="btn orange" href="#">VIEW ALL EVENTS &rsaquo;</a></div></div>',
                bg="#ffffff",
            ),
        ],
    },
    "newsletter": {
        "title": "Newsletter",
        "build": lambda: [
            hero("nl", "NEWSLETTER", "Subscribe to the CIWA Grapevine — quarterly updates on programs, events, employers, and stories from our community.", "welcome/collage.png", cta1=("SUBSCRIBE","#subscribe")),
            html_section("nl", "body",
                SHARED_CSS + '<div class="ciwa-c" id="subscribe"><h2 class="center" style="margin-bottom:32px;">SUBSCRIBE TO OUR NEWSLETTER</h2><form class="form" action="#" method="post" style="background:#fff;"><div class="form-row"><label><span>First Name</span><input type="text" name="first_name"></label><label><span>Email Address</span><input type="email" name="email" required></label></div><div style="text-align:center;"><button type="submit" class="form-submit">SUBSCRIBE TO NEWSLETTER &rsaquo;</button></div></form><div class="grid-4 wrap-1320" style="margin-top:64px;">'
                + ''.join(
                    f'<div class="card" style="padding:22px 20px;"><h4 style="font-size:16px;color:{c};">CIWA GRAPEVINE</h4><p style="font-size:12px;color:#8a7a87;margin:0;">July 2025</p><p>Updates on programs, upcoming events, employer partnerships, and member stories.</p><a href="#issue" style="color:#6a1753;font-size:12px;text-decoration:underline;">View Newsletter &rsaquo;</a></div>'
                    for c in ("#e22371","#f68b3c","#ff6e6e","#6a1753") * 2
                )
                + '</div></div>',
                bg="#fdf6ef",
            ),
        ],
    },
    "useful-links": {
        "title": "Useful Links",
        "build": lambda: page_list(
            "ul", "RESOURCES",
            "A curated collection of trusted resources, programs, and services to help immigrant women and families build a strong life in Calgary.",
            "welcome/collage.png",
            "IMPORTANT RESOURCES", "AND LINKS",
            [
                ("Alberta Association of Immigrant Serving Agencies", "#"),
                ("Alberta Association of Services for Children and Families", "#"),
                ("Alberta Employment and Immigration", "#"),
                ("Alberta Human Rights and Citizenship Commission", "#"),
                ("Alberta Network of Immigrant Women", "#"),
                ("Alberta Labour", "#"),
                ("Calgary and Area Child and Family Services Authority", "#"),
                ("Calgary Board of Education", "#"),
                ("Calgary Catholic Immigration Society", "#"),
                ("Centre for Newcomers", "#"),
                ("Calgary Catholic School District", "#"),
                ("Canadian Council for Refugees", "#"),
                ("Calgary Immigrant Educational Society", "#"),
                ("Calgary Legal Guidance", "#"),
                ("Calgary Multicultural Centre", "#"),
                ("Canadian Immigrant Magazine", "#"),
                ("Changing Together: A Centre for Immigrant Women", "#"),
            ],
        ),
    },
    "contact": {
        "title": "Contact",
        "build": lambda: [
            hero("cnt", "CONTACT", "Get in touch — our team is ready to help newcomers, partners, and supporters connect with the right CIWA program or service.", "contact/group.png", cta1=("LEARN MORE","#contact-form")),
            html_section("cnt", "body",
                SHARED_CSS + '<div class="ciwa-c" id="contact-form"><h2 class="center" style="margin-bottom:14px;">CONTACT FORM</h2><p class="center lead wrap-880">Thank you for contacting us. Please fill out the form below and our staff will contact you to find out how we can help.</p><form class="form" action="#" method="post" style="background:#fff;padding:32px;border-radius:14px;box-shadow:0 2px 8px rgba(0,0,0,.05);"><div class="form-row"><label><span>First Name:</span><input type="text" name="first_name"></label><label><span>Last Name:</span><input type="text" name="last_name"></label></div><div class="form-row"><label><span>Email Address:</span><input type="email" name="email"></label><label><span>Phone:</span><input type="tel" name="phone"></label></div><div class="form-row"><label><span>Language Spoken:</span><input type="text" name="language"></label><label><span>How would you like us to contact you? *</span><div style="display:flex;gap:18px;padding:12px 0;"><label style="display:inline-flex;gap:8px;align-items:center;font-size:15px;color:#1a1a1a;flex:none;"><input type="radio" name="contact_pref" value="email"> Email</label><label style="display:inline-flex;gap:8px;align-items:center;font-size:15px;color:#1a1a1a;flex:none;"><input type="radio" name="contact_pref" value="phone"> Phone</label></div></label></div><div class="form-row"><label class="full"><span>How can we help you? *</span><textarea name="message" rows="5"></textarea></label></div><div class="form-row"><label class="full"><span>Subscribe to CIWA\'s Newsletter?</span><div style="display:flex;gap:18px;padding:12px 0;"><label style="display:inline-flex;gap:8px;align-items:center;font-size:15px;color:#1a1a1a;flex:none;"><input type="radio" name="newsletter" value="yes"> Yes</label><label style="display:inline-flex;gap:8px;align-items:center;font-size:15px;color:#1a1a1a;flex:none;"><input type="radio" name="newsletter" value="no"> No</label></div></label></div><div style="display:flex;justify-content:flex-end;"><button type="submit" class="form-submit">SUBMIT &rsaquo;</button></div></form><img src="{ASSETS}/map/map.png" alt="Calgary office map" style="display:block;max-width:1320px;margin:48px auto 0;width:100%;height:auto;border-radius:14px;"></div>',
                bg="#ffffff",
            ),
        ],
    },
}


# ---------------------------------------------------------------------------
# Build all
# ---------------------------------------------------------------------------

def main():
    count = 0
    for slug, page in PAGES.items():
        content = page["build"]()
        template = {
            "version": "0.4",
            "title": page["title"],
            "type": "page",
            "page_settings": {"hide_title": "yes"},
            "content": content,
        }
        out_path = os.path.join(OUT_DIR, f"{slug}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2)
        size = os.path.getsize(out_path)
        print(f"  {slug:30s}  {len(content):2d} sections  {size:>7d} bytes")
        count += 1
    print(f"\nGenerated {count} page templates in {OUT_DIR}")


if __name__ == "__main__":
    main()
