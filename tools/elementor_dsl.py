"""
Tiny Python DSL for building Elementor JSON template trees.

Wraps Elementor's native widget primitives so pages can be composed in
~30 lines instead of ~300 lines of raw JSON per page.
"""

import hashlib

_id_counter = 0
def _id(prefix=""):
    global _id_counter
    _id_counter += 1
    return f"{prefix}{_id_counter:04d}" if prefix else f"e{_id_counter:04d}"


# ---------------------------------------------------------------------------
# Containers
# ---------------------------------------------------------------------------

def section(*, bg="#ffffff", padding=(80, 32, 80, 32), content_width=1320, structure="10",
            gap="default", inner=False, extra_settings=None, columns=None, id_=None):
    """Section (or inner-section). `columns` is a list of column() outputs."""
    settings = {
        "structure": structure,
        "background_background": "classic" if bg else None,
        "background_color": bg,
        "padding": _spacing(*padding),
        "content_width": {"unit": "px", "size": content_width},
        "gap": gap,
    }
    settings = {k: v for k, v in settings.items() if v is not None}
    if extra_settings:
        settings.update(extra_settings)
    return {
        "id": id_ or _id("s"),
        "elType": "section",
        "isInner": inner,
        "settings": settings,
        "elements": columns or [],
    }


def column(*, size=100, vertical_align="top", bg=None, border_left_color=None,
           border_radius=None, padding=None, box_shadow=False,
           min_height=None, extra_settings=None, widgets=None, id_=None):
    """Elementor column. Use bg/border/padding to style as a card."""
    settings = {"_column_size": size, "_inline_size": None, "content_position": vertical_align}
    if bg:
        settings.update({
            "background_background": "classic",
            "background_color": bg,
        })
    if border_left_color:
        settings.update({
            "border_border": "solid",
            "border_width": _spacing(0, 0, 0, 6),
            "border_color": border_left_color,
        })
    else:
        # default subtle border for cards
        if bg and bg != "transparent":
            settings.update({
                "border_border": "solid",
                "border_width": _spacing(1, 1, 1, 1),
                "border_color": "#e6dce4",
            })
    if border_radius is not None:
        settings["border_radius"] = _spacing(border_radius, border_radius, border_radius, border_radius)
    if padding:
        settings["padding"] = _spacing(*padding)
    if box_shadow:
        settings.update({
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {
                "horizontal": 0, "vertical": 2, "blur": 6, "spread": 0,
                "color": "rgba(0,0,0,0.04)",
            },
        })
    if min_height:
        settings["min_height"] = {"unit": "px", "size": min_height}
    if extra_settings:
        settings.update(extra_settings)
    return {
        "id": id_ or _id("c"),
        "elType": "column",
        "settings": settings,
        "elements": widgets or [],
    }


# ---------------------------------------------------------------------------
# Widgets
# ---------------------------------------------------------------------------

def heading(title, *, level="h2", color="#6a1753", size=44, weight="400",
            family="Cormorant Garamond", letter_spacing=-1, align="left",
            transform="uppercase", line_height=1.1, margin=None, id_=None):
    s = {
        "title": title,
        "header_size": level,
        "align": align,
        "title_color": color,
        "typography_typography": "custom",
        "typography_font_family": family,
        "typography_font_size": {"unit": "px", "size": size},
        "typography_font_weight": weight,
        "typography_letter_spacing": {"unit": "px", "size": letter_spacing},
        "typography_text_transform": transform,
        "typography_line_height": {"unit": "em", "size": line_height},
    }
    if margin:
        s["_margin"] = _spacing(*margin)
    return _widget("heading", s, id_)


def text(html_content, *, color="#4a4a4a", family="Inter", size=16, line_height=1.6,
         align=None, margin=None, max_width=None, id_=None):
    s = {
        "editor": html_content,
        "text_color": color,
        "typography_typography": "custom",
        "typography_font_family": family,
        "typography_font_size": {"unit": "px", "size": size},
        "typography_line_height": {"unit": "em", "size": line_height},
    }
    if align:
        s["align"] = align
    if margin:
        s["_margin"] = _spacing(*margin)
    if max_width:
        s["_css_max-width"] = max_width
    return _widget("text-editor", s, id_)


def button(text_, link="#", *, bg="#f68b3c", text_color="#ffffff", family="Cormorant Garamond",
           size_px=14, padding=(13, 28, 13, 28), radius=8, letter_spacing=1.5,
           align="left", outline=False, outline_color="#6a1753", id_=None):
    if outline:
        bg = "rgba(0,0,0,0)"
        text_color = outline_color
        border_settings = {
            "border_border": "solid",
            "border_width": _spacing(2, 2, 2, 2),
            "border_color": outline_color,
        }
    else:
        border_settings = {}
    s = {
        "text": text_,
        "link": {"url": link, "is_external": "", "nofollow": ""},
        "align": align,
        "background_color": bg,
        "button_text_color": text_color,
        "typography_typography": "custom",
        "typography_font_family": family,
        "typography_font_size": {"unit": "px", "size": size_px},
        "typography_font_weight": "400",
        "typography_letter_spacing": {"unit": "px", "size": letter_spacing},
        "typography_text_transform": "uppercase",
        "border_radius": _spacing(radius, radius, radius, radius),
        "text_padding": _spacing(*padding),
        **border_settings,
    }
    return _widget("button", s, id_)


def image(url, *, radius=18, align="center", width_px=None, id_=None):
    s = {
        "image": {"url": url, "id": ""},
        "image_size": "full",
        "align": align,
    }
    if radius:
        s["image_border_radius"] = _spacing(radius, radius, radius, radius)
    if width_px:
        s["width"] = {"unit": "px", "size": width_px}
    return _widget("image", s, id_)


def spacer(height_px, id_=None):
    return _widget("spacer", {"space": {"unit": "px", "size": height_px}}, id_)


def html(raw, id_=None):
    return _widget("html", {"html": raw}, id_)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _widget(widget_type, settings, id_):
    return {
        "id": id_ or _id("w"),
        "elType": "widget",
        "widgetType": widget_type,
        "settings": settings,
    }


def _spacing(top, right, bottom, left, unit="px"):
    return {
        "unit": unit, "isLinked": False,
        "top": str(top), "right": str(right),
        "bottom": str(bottom), "left": str(left),
    }


def template(title, sections, type_="page"):
    return {
        "version": "0.4",
        "title": title,
        "type": type_,
        "page_settings": {"hide_title": "yes"},
        "content": sections,
    }
