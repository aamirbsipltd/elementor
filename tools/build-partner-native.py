#!/usr/bin/env python3
"""
Path B (native Elementor widgets) rebuild of Partner With Us.

Every section uses native Elementor widgets where free Elementor has a
matching widget. Forms and the (FOR BUSINESS / FOR COMMUNITY PARTNERS)
tab toggle fall back to Custom HTML widgets — free Elementor has no
Form or Tabs widget (Pro-only).

Cards (Why-Partner, FOR BUSINESS 2x2, Sponsor/Talent 2-up) are rebuilt
as Elementor Inner Sections with styled columns acting as cards. Each
card column has white bg, colored left border, padding, box-shadow.
Inside each column: Image (icon) + Heading + Text widgets — fully
editable in the Elementor UI.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elementor_dsl import (
    section, column, heading, text, button, image, spacer, html, template,
)

ASSETS = "{ASSETS}"  # placeholder, replaced at import time

CTA_PADDING = (13, 28, 13, 28)
CARD_PAD    = (28, 28, 28, 28)
CARD_RADIUS = 14


def hero():
    return section(
        bg="#fce7f0", padding=(80, 32, 96, 32), content_width=1320,
        structure="20", gap="extended",
        columns=[
            column(size=50, vertical_align="center", widgets=[
                heading("PARTNER WITH US", level="h1", size=56, letter_spacing=-1.3,
                        margin=(0, 0, 20, 0)),
                text("<p>Join us in empowering immigrant and refugee women in Calgary. "
                     "Together we open doors to employment, community, and lasting impact.</p>",
                     color="#1a1a1a", size=17,
                     margin=(0, 0, 28, 0)),
                # Two buttons in an inner section row
                section(inner=True, bg=None, padding=(0, 0, 0, 0), structure="20",
                        content_width=600, columns=[
                            column(size=50, widgets=[
                                button("JOIN NOW ›", "#partner-contact",
                                       bg="#f68b3c", padding=CTA_PADDING),
                            ]),
                            column(size=50, widgets=[
                                button("LEARN MORE ›", "#why-partner",
                                       outline=True, padding=CTA_PADDING),
                            ]),
                        ]),
            ]),
            column(size=50, vertical_align="center", widgets=[
                image(f"{ASSETS}/contact/group.png", radius=18, align="center"),
            ]),
        ],
    )


def why_partner_section():
    """3-card 'Why Partner' grid as native Elementor columns styled as cards."""
    cards = [
        ("ciwa-final/icon-1.svg", "#6a1753", "Support Thousands",
         "You actively support thousands of immigrant women in building successful lives and contribute to community wellbeing."),
        ("ciwa-final/icon-2.svg", "#f68b3c", "Diversity & Inclusion",
         "You demonstrate your organization's commitment to diversity and inclusion while addressing critical workforce gaps."),
        ("ciwa-final/icon-3.svg", "#e22371", "Skilled Professionals",
         "You gain access to a wide pool of skilled professionals ready to contribute meaningfully to your business."),
    ]
    # Build card columns
    card_columns = []
    for icon_slug, accent, title, body in cards:
        # accent is used as title color (no left border on Why-cards per Figma)
        card_columns.append(column(
            size=33, bg="#ffffff", border_radius=CARD_RADIUS, padding=(36, 28, 36, 28),
            box_shadow=True,
            widgets=[
                image(f"{ASSETS}/programs/{icon_slug.split('/')[-1]}", radius=0, align="left",
                      width_px=48),
                heading(title, level="h3", size=22, color=accent,
                        letter_spacing=0.4, margin=(8, 0, 4, 0)),
                text(f"<p>{body}</p>", size=15, line_height=1.6),
            ],
        ))

    return section(
        bg="#fdf6ef", padding=(80, 32, 80, 32), content_width=1320,
        structure="10",
        extra_settings={"_element_id": "why-partner"},
        columns=[column(size=100, widgets=[
            heading("WHY PARTNER <span style='color:#ff6e6e'>WITH US?</span>",
                    level="h2", align="center", size=44, letter_spacing=-1,
                    margin=(0, 0, 16, 0)),
            text("<p style='text-align:center;max-width:880px;margin:0 auto 48px;'>"
                 "CIWA offers diverse partnership opportunities tailored to your organization's "
                 "goals and values. Discover how you can make a meaningful impact.</p>",
                 size=17, line_height=1.6, align="center",
                 margin=(0, 0, 0, 0)),
            section(inner=True, bg=None, padding=(0, 0, 0, 0), structure="33",
                    content_width=1320, gap="extended",
                    columns=card_columns),
        ])],
    )


def business_cards_section():
    """4-card 2x2 'FOR BUSINESS' grid + work banner + 2-up. Tab nav stays HTML."""
    business = [
        ("#6a1753", "Networking with Newcomers",
         "<p>Participate in networking events to meet immigrant women entering the Canadian workforce. "
         "Help newcomers navigate resumes, interviews, and job applications.</p>"),
        ("#e22371", "Host a Work Placement or Practicum",
         "<p>Provide work placements for immigrant women enrolled in CIWA programs. Offer practical "
         "Canadian work experience, helping participants overcome employment barriers.</p>"),
        ("#6a1753", "Hire Graduates",
         "<p>Employ qualified CIWA alumnae trained in childcare, customer service, office administration, "
         "and more. Support economic security for immigrant women and their families.</p>"),
        ("#e22371", "Refer Job Seekers",
         "<p>Direct immigrant women not yet job-ready to CIWA's bridge-to-work programs. Free training in "
         "retail, food service, security, hospitality, and interpretation.</p>"),
    ]

    # Each pair of cards is one row (Inner Section with 2 cols).
    rows = []
    for r in range(0, 4, 2):
        rows.append(section(
            inner=True, bg=None, padding=(0, 0, 0, 0), structure="20", gap="extended",
            content_width=1320,
            columns=[
                _business_card(*business[r]),
                _business_card(*business[r + 1]),
            ],
        ))

    # Tab nav as HTML widget (Tabs widget is Pro-only)
    tab_nav_html = (
        "<style>"
        ".pwu-tabs-nav{max-width:880px;margin:0 auto 32px;border-bottom:1px solid #d6c8d4;display:flex;gap:0}"
        ".pwu-tab{padding:18px 24px;flex:1;border-bottom:3px solid transparent;margin-bottom:-1px;"
        "font-family:'Cormorant Garamond',serif;font-size:16px;letter-spacing:1px;color:#8a7a87;"
        "text-transform:uppercase;text-align:center;}"
        ".pwu-tab.active{color:#6a1753;border-bottom-color:#6a1753}"
        "</style>"
        "<div class='pwu-tabs-nav'><div class='pwu-tab active'>FOR BUSINESS</div>"
        "<div class='pwu-tab'>FOR COMMUNITY PARTNERS</div></div>"
    )

    # Work-experience banner — single styled column
    work_section = section(
        inner=True, bg=None, padding=(0, 0, 0, 0), structure="10", content_width=1320,
        columns=[column(
            size=100, bg="#ffffff", border_left_color="#5bbdad",
            border_radius=CARD_RADIUS, padding=(36, 36, 36, 36), box_shadow=True,
            widgets=[
                heading("Host a Work Experience", level="h3", size=22, color="#5bbdad",
                        letter_spacing=0.4, margin=(0, 0, 14, 0)),
                text("<p>CIWA works with employers to host work placements for employment-ready "
                     "immigrant women. Employers benefit from a motivated workforce, while participants "
                     "gain practical Canadian work experience that opens doors to long-term careers.</p>",
                     size=16, line_height=1.6, margin=(0, 0, 20, 0)),
                html(
                    "<style>.pwu-tags{display:flex;flex-wrap:wrap;gap:10px}"
                    ".pwu-tag{background:#eaf6f3;color:#2d6f64;padding:6px 14px;border-radius:999px;"
                    "font-size:13px;letter-spacing:0.5px;text-transform:uppercase;font-family:'Inter',sans-serif}</style>"
                    "<div class='pwu-tags'>"
                    "<span class='pwu-tag'>Accounting</span>"
                    "<span class='pwu-tag'>Office administration</span>"
                    "<span class='pwu-tag'>Management</span>"
                    "<span class='pwu-tag'>Sales and Marketing</span>"
                    "<span class='pwu-tag'>IT</span>"
                    "<span class='pwu-tag'>Childcare</span>"
                    "<span class='pwu-tag'>Retail</span>"
                    "</div>"
                ),
            ],
        )],
    )

    # 2-up Sponsor / Diverse Talent
    twoup = section(
        inner=True, bg=None, padding=(0, 0, 0, 0), structure="20", gap="extended",
        content_width=1320,
        columns=[
            column(size=50, bg="#ffffff", border_left_color="#f68b3c",
                   border_radius=CARD_RADIUS, padding=CARD_PAD, box_shadow=True,
                   widgets=[
                       heading("Be a Corporate or Community Sponsor", level="h3", size=22,
                               color="#f68b3c", letter_spacing=0.4, margin=(0, 0, 12, 0)),
                       text("<p>Amplify CIWA's impact by sponsoring initiatives that break barriers for "
                            "immigrant women. Host space for events or provide in-kind services to support programs.</p>",
                            size=15, line_height=1.6),
                   ]),
            column(size=50, bg="#ffffff", border_left_color="#6a1753",
                   border_radius=CARD_RADIUS, padding=CARD_PAD, box_shadow=True,
                   widgets=[
                       heading("Access Diverse Talent", level="h3", size=22,
                               color="#6a1753", letter_spacing=0.4, margin=(0, 0, 12, 0)),
                       text("<p>Join CIWA's free platform for employers, \"Diverse Workforce,\" to connect "
                            "with qualified immigrant women across sectors.</p>",
                            size=15, line_height=1.6),
                   ]),
        ],
    )

    return section(
        bg="#ffffff", padding=(64, 32, 96, 32), content_width=1320, structure="10",
        columns=[column(size=100, widgets=[
            html(tab_nav_html),
            text("<p style='text-align:center;max-width:1100px;margin:0 auto 48px;'>"
                 "CIWA works with over 150 business partners each and every year, making a significant "
                 "impact by volunteering time, knowledge, space, or offering employment to newcomers "
                 "in Calgary.</p>",
                 size=17, line_height=1.6, align="center", margin=(0, 0, 0, 0)),
            rows[0],
            spacer(28),
            rows[1],
            spacer(56),
            work_section,
            spacer(56),
            twoup,
        ])],
    )


def _business_card(accent, title, body_html):
    return column(
        size=50, bg="#ffffff", border_left_color=accent,
        border_radius=CARD_RADIUS, padding=CARD_PAD, box_shadow=True,
        widgets=[
            heading(title, level="h3", size=21, color=accent,
                    letter_spacing=0.4, margin=(0, 0, 12, 0)),
            text(body_html, size=15, line_height=1.6),
        ],
    )


def spotlight():
    return section(
        bg="#6a1753", padding=(80, 32, 80, 32), structure="10",
        columns=[column(size=100, widgets=[
            heading("BUSINESS SPOTLIGHT", level="h2", color="#ffffff",
                    size=48, letter_spacing=-1, align="center",
                    margin=(0, 0, 14, 0)),
            text("<p style='text-align:center;color:rgba(255,255,255,.9);'>"
                 "See how our business partners are making a difference.</p>",
                 align="center", color="rgba(255,255,255,0.9)",
                 margin=(0, 0, 28, 0)),
            # button widget centered
            section(inner=True, bg=None, padding=(0, 0, 0, 0), structure="10",
                    columns=[column(size=100, extra_settings={"align": "center"}, widgets=[
                        button("VIEW BUSINESS PARTNERS ›", "#partners",
                               bg="#f68b3c", padding=(14, 28, 14, 28), align="center"),
                    ])]),
        ])],
    )


def contact_form():
    """Contact form — HTML widget (free Elementor has no Form widget)."""
    form_html = (
        "<style>"
        ".pwu-form{max-width:880px;margin:0 auto;display:flex;flex-direction:column;gap:22px;font-family:'Inter',sans-serif}"
        ".pwu-form-row{display:flex;flex-wrap:wrap;gap:22px}"
        ".pwu-field{flex:1 1 calc(50% - 11px);display:flex;flex-direction:column;gap:8px;min-width:220px}"
        ".pwu-field.full{flex:1 1 100%}"
        ".pwu-field label{font-family:'Cormorant Garamond',serif;font-size:13px;letter-spacing:1px;text-transform:uppercase;color:#6a1753}"
        ".pwu-field input,.pwu-field select,.pwu-field textarea{background:#fff;border:1px solid #d6c8d4;border-radius:8px;padding:12px 14px;font-size:15px;color:#1a1a1a;font-family:inherit;width:100%;box-sizing:border-box}"
        ".pwu-field textarea{resize:vertical;min-height:140px}"
        ".pwu-form-actions{display:flex;justify-content:flex-end}"
        ".pwu-submit{background:#6a1753;color:#fff;border:0;padding:14px 32px;border-radius:8px;font-family:'Cormorant Garamond',serif;font-size:15px;text-transform:uppercase;letter-spacing:1.5px;cursor:pointer}"
        ".pwu-submit:hover{background:#4f0f3e}"
        "</style>"
        "<form class='pwu-form' action='#' method='post'>"
        "<div class='pwu-form-row'>"
        "<div class='pwu-field'><label>First Name:</label><input type='text' name='first_name'></div>"
        "<div class='pwu-field'><label>Email Address:</label><input type='email' name='email'></div>"
        "</div>"
        "<div class='pwu-form-row'><div class='pwu-field full'><label>Organization:</label><input type='text' name='organization'></div></div>"
        "<div class='pwu-form-row'><div class='pwu-field full'><label>Partnership Type:</label>"
        "<select name='partnership_type'><option value=''>Select…</option><option>Business</option>"
        "<option>Community Partner</option><option>Sponsor</option></select></div></div>"
        "<div class='pwu-form-row'><div class='pwu-field full'><label>Message:</label>"
        "<textarea name='message' rows='6'></textarea></div></div>"
        "<div class='pwu-form-actions'><button type='submit' class='pwu-submit'>Send Message ›</button></div>"
        "</form>"
    )
    return section(
        bg="#ffffff", padding=(80, 32, 80, 32), content_width=1320,
        extra_settings={"_element_id": "partner-contact"},
        columns=[column(size=100, widgets=[
            heading("CONTACT <span style='color:#ff6e6e'>US</span>",
                    level="h2", align="center", size=48, letter_spacing=-1,
                    margin=(0, 0, 12, 0)),
            text("<p style='text-align:center;color:#4a4a4a;'>Explore partnership opportunities today!</p>",
                 align="center", margin=(0, 0, 40, 0)),
            html(form_html),
        ])],
    )


def main():
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "templates", "elementor", "partner-with-us.json")
    tpl = template("Partner With Us", [
        hero(),
        why_partner_section(),
        business_cards_section(),
        spotlight(),
        contact_form(),
    ])
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tpl, f, indent=2)
    print(f"Wrote {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    main()
