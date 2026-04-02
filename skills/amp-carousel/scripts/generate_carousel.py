#!/usr/bin/env python3
"""
Amplitude LinkedIn Carousel Generator
Generates 1080x1080 PNG slides from a JSON slide spec.

Usage:
  python3 generate_carousel.py --slides '<JSON array>' --output /path/to/output/dir
  python3 generate_carousel.py --slides-file slides.json --output /path/to/output/dir
"""

import argparse
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# ── Brand colors ──────────────────────────────────────────────────────────────
C = {
    "black":     "#000000",
    "white":     "#FFFFFF",
    "blue":      "#0052F2",
    "dark_blue": "#001A4F",
    "lilac":     "#6980FF",
    "violet":    "#A373FF",
    "pink":      "#FF7D78",
    "red":       "#F23845",
    "g100":      "#13171A",
    "g90":       "#242A2E",
    "g80":       "#373D42",
    "g70":       "#50565B",
    "g60":       "#697077",
    "g50":       "#868D95",
    "g40":       "#9FA5AD",
    "g30":       "#B9BFC7",
    "g20":       "#D5D9E0",
    "g10":       "#F2F4F8",
    # Light background equivalents
    "l_card":    "#F2F4F8",
    "l_card2":   "#E4E8EE",
    "l_border":  "#D5D9E0",
}

COLOR_NAMES = {
    "blue": C["blue"], "lilac": C["lilac"], "violet": C["violet"],
    "pink": C["pink"], "white": C["white"], "red": C["red"],
}

W, H = 1080, 1080
FONT_DIR = "/usr/share/fonts/truetype/google-fonts"
PAD = 80       # left/right padding
TOP = 120      # top content start (below logo)
BOTTOM = 80    # bottom padding

# Logo resolution order:
#   1. assets/ folder bundled alongside this script (skill-local)
#   2. "amp brand" folder in the Agentwork workspace (absolute fallback)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_ASSETS_DIR = os.path.join(_SCRIPT_DIR, "..", "assets")
_WORKSPACE_LOGO_DIR = os.path.join(
    os.path.dirname(_SCRIPT_DIR),  # up from scripts/ → amp-carousel/
    "..", "..", "..", "..", "..",   # up to mnt/
    "Agentwork", "amp brand", "Amplitude Logo", "Full", "PNG (RGB)"
)

def _find_logo(name):
    """Find a logo file, preferring assets/ then workspace fallback."""
    local = os.path.join(_ASSETS_DIR, name)
    if os.path.exists(local):
        return local
    workspace = os.path.normpath(os.path.join(_WORKSPACE_LOGO_DIR, name))
    if os.path.exists(workspace):
        return workspace
    return None

LOGO_WHITE = _find_logo("logo_amplitude_full_white_RGB.png")
LOGO_BLACK = _find_logo("logo_amplitude_full_black_RGB.png")

# Target logo width on slide
LOGO_W = 180


def rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def font(weight="Regular", size=40):
    path = os.path.join(FONT_DIR, f"Poppins-{weight}.ttf")
    return ImageFont.truetype(path, size)


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def color_for_name(name):
    return rgb(COLOR_NAMES.get(name, C["blue"]))


# ── Theme helpers ─────────────────────────────────────────────────────────────

def is_dark(theme):
    return theme == "dark"


def bg_color(theme):
    return rgb(C["black"]) if is_dark(theme) else rgb(C["white"])


def fg_color(theme):
    """Primary text color"""
    return rgb(C["white"]) if is_dark(theme) else rgb(C["black"])


def fg_secondary(theme):
    """Secondary / subdued text"""
    return rgb(C["g40"]) if is_dark(theme) else rgb(C["g60"])


def fg_muted(theme):
    """Muted label text"""
    return rgb(C["g70"]) if is_dark(theme) else rgb(C["g50"])


def card_fill(theme):
    return rgb(C["g100"]) if is_dark(theme) else rgb(C["l_card"])


def card_border(theme):
    return rgb(C["g90"]) if is_dark(theme) else rgb(C["l_border"])


def divider_color(theme):
    return rgb(C["g90"]) if is_dark(theme) else rgb(C["l_border"])


def label_color(theme):
    return rgb(C["blue"])  # always blue


# ── Base slide setup ──────────────────────────────────────────────────────────

def new_slide(theme="dark"):
    img = Image.new("RGB", (W, H), bg_color(theme))
    draw = ImageDraw.Draw(img)
    _draw_gradient_bar(draw)
    return img, draw


def _draw_gradient_bar(draw):
    stops = [rgb(C["blue"]), rgb(C["lilac"]), rgb(C["violet"])]
    for x in range(W):
        t = x / (W - 1)
        if t < 0.5:
            c = lerp_color(stops[0], stops[1], t / 0.5)
        else:
            c = lerp_color(stops[1], stops[2], (t - 0.5) / 0.5)
        draw.line([(x, 0), (x, 7)], fill=c)


def add_logo(img, draw, theme="dark"):
    """Paste the real Amplitude logo PNG, sized to LOGO_W wide."""
    logo_path = LOGO_WHITE if is_dark(theme) else LOGO_BLACK
    try:
        if not logo_path:
            raise FileNotFoundError("Logo not found")
        logo_img = Image.open(logo_path).convert("RGBA")
        orig_w, orig_h = logo_img.size
        target_w = LOGO_W
        target_h = int(orig_h * target_w / orig_w)
        logo_img = logo_img.resize((target_w, target_h), Image.LANCZOS)
        # Vertically center in the header zone (38–82px)
        logo_y = int(38 + (44 - target_h) / 2)
        img.paste(logo_img, (PAD, logo_y), logo_img)
    except Exception:
        # Fallback to drawn logo if file missing
        draw.rounded_rectangle([PAD, 38, PAD + 44, 82], radius=10, fill=rgb(C["blue"]))
        draw.text((PAD + 10, 43), "A", fill=rgb(C["white"]), font=font("Bold", 24))
        draw.text((PAD + 56, 48), "Amplitude", fill=fg_secondary(theme), font=font("Bold", 20))


def add_slide_number(draw, num, total, theme="dark"):
    f = font("Medium", 18)
    text = f"{num} / {total}"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text((W - PAD - tw, 52), text, fill=fg_muted(theme), font=f)


# ── Layout helpers ─────────────────────────────────────────────────────────────

def center_x(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return (W - (bbox[2] - bbox[0])) // 2


def draw_centered(draw, y, text, fnt, color):
    x = center_x(draw, text, fnt)
    draw.text((x, y), text, fill=color, font=fnt)
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return y + (bbox[3] - bbox[1])


def draw_label(draw, text, y=TOP, theme="dark"):
    if not text:
        return y
    f = font("Bold", 18)
    cx = center_x(draw, text, f)
    draw.text((cx, y), text, fill=label_color(theme), font=f)
    return y + 30


def draw_headline(draw, lines, highlights, y, size=48, highlight_color="blue", theme="dark"):
    f = font("Bold", size)
    hc = rgb(COLOR_NAMES.get(highlight_color, C["blue"]))
    for i, line in enumerate(lines):
        color = hc if (i < len(highlights) and highlights[i]) else fg_color(theme)
        y = draw_centered(draw, y, line, f, color) + 8
    return y + 8


def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_glow(img, alpha=12, radius=280, theme="dark"):
    """Subtle blue center glow — only on dark slides."""
    if not is_dark(theme):
        return
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(radius, 0, -1):
        a = int(alpha * (r / radius))
        gd.ellipse([W//2 - r, H//2 - r, W//2 + r, H//2 + r], fill=(0, 82, 242, a))
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    merged = Image.alpha_composite(base, glow).convert("RGB")
    img.paste(merged)


def wrap_text(draw, text, fnt, max_width):
    words = text.split()
    lines, current = [], ""
    for w in words:
        test = f"{current} {w}".strip()
        bbox = draw.textbbox((0, 0), test, font=fnt)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def draw_wrapped_centered(draw, text, fnt, color, y, max_width=W - PAD * 2, line_gap=10):
    lines = wrap_text(draw, text, fnt, max_width)
    for line in lines:
        y = draw_centered(draw, y, line, fnt, color) + line_gap
    return y


def measure_wrapped(draw, text, fnt, max_width=W - PAD * 2, line_gap=10):
    """Return height of wrapped text block."""
    lines = wrap_text(draw, text, fnt, max_width)
    total = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        total += (bbox[3] - bbox[1]) + line_gap
    return total


def measure_headline(draw, lines, size=48):
    f = font("Bold", size)
    total = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=f)
        total += (bbox[3] - bbox[1]) + 8
    return total + 8


# ── Slide renderers ────────────────────────────────────────────────────────────

def render_title(draw, img, s, num, total, theme="dark"):
    draw_glow(img, alpha=14, radius=300, theme=theme)
    draw = ImageDraw.Draw(img)
    _draw_gradient_bar(draw)

    lines = s.get("headline", [])
    hook = s.get("hook", "")
    subtitle = s.get("subtitle", "")
    approx_h = (36 if hook else 0) + measure_headline(draw, lines, 72) + (80 if subtitle else 0)
    y = max(TOP + 40, (H - approx_h) // 2 - 20)

    if hook:
        f_hook = font("Bold", 18)
        cx = center_x(draw, hook, f_hook)
        draw.text((cx, y), hook, fill=rgb(C["blue"]), font=f_hook)
        y += 36

    highlights = s.get("headline_highlight", [False] * len(lines))
    f_h = font("Bold", 72)
    for i, line in enumerate(lines):
        color = rgb(C["blue"]) if (i < len(highlights) and highlights[i]) else fg_color(theme)
        y = draw_centered(draw, y, line, f_h, color) + 10
    y += 16

    if subtitle:
        draw_wrapped_centered(draw, subtitle, font("Regular", 24), fg_secondary(theme), y, W - 200)

    if s.get("swipe", True):
        f_sw = font("Medium", 17)
        draw_centered(draw, H - 68, "SWIPE →", f_sw, fg_muted(theme))


def render_stat(draw, s, num, total, theme="dark"):
    ctx_lines = s.get("context", [])
    label = s.get("label", "")
    unit = s.get("big_unit", "")
    date = s.get("date", "")
    approx_h = (30 if label else 0) + 180 + (50 if unit else 0) + (40 if date else 0) + 60 + len(ctx_lines) * 44
    usable = H - BOTTOM - TOP
    y = max(TOP, TOP + (usable - approx_h) // 2)

    if label:
        y = draw_label(draw, label, y=y, theme=theme) + 16

    big = s.get("big_number", "")
    f_big = font("Bold", 160)
    draw_centered(draw, y, big, f_big, rgb(C["blue"]))
    y += 180

    if unit:
        y = draw_centered(draw, y, unit, font("Bold", 36), rgb(C["lilac"])) + 12

    if date:
        y = draw_centered(draw, y, date, font("Medium", 24), fg_color(theme)) + 32

    draw.line([(PAD + 80, y), (W - PAD - 80, y)], fill=divider_color(theme), width=1)
    y += 28

    for i, line in enumerate(ctx_lines):
        fnt = font("Bold", 20) if i == len(ctx_lines) - 1 else font("Regular", 20)
        clr = fg_secondary(theme) if i == len(ctx_lines) - 1 else fg_muted(theme)
        draw_wrapped_centered(draw, line, fnt, clr, y)
        y += 44


def render_text(draw, s, num, total, theme="dark"):
    lines = s.get("headline", [])
    body = s.get("body", "")
    callout = s.get("callout", "")
    label = s.get("label", "")

    approx_h = (30 if label else 0) + measure_headline(draw, lines, 46) + 16
    if body:
        approx_h += measure_wrapped(draw, body, font("Regular", 26), W - 160, 14) + 20
    if callout:
        approx_h += 28 + 100
    usable = H - BOTTOM - TOP
    y = max(TOP, TOP + (usable - approx_h) // 2)

    if label:
        y = draw_label(draw, label, y=y, theme=theme) + 16

    highlights = s.get("headline_highlight", [False] * len(lines))
    y = draw_headline(draw, lines, highlights, y, size=46, theme=theme)
    y += 16

    if body:
        y = draw_wrapped_centered(draw, body, font("Regular", 26), fg_secondary(theme), y, W - 160, line_gap=14)

    if callout:
        y += 28
        box_h = 100
        rounded_rect(draw, [PAD, y, W - PAD, y + box_h], 16,
                     fill=card_fill(theme), outline=card_border(theme))
        draw_wrapped_centered(draw, callout, font("Medium", 22), fg_color(theme),
                              y + (box_h - 28) // 2, W - PAD * 2 - 60)


def render_grid(draw, s, num, total, theme="dark"):
    label = s.get("label", "")
    lines = s.get("headline", [])
    items = s.get("items", [])[:4]

    card_w = (W - PAD * 2 - 24) // 2
    # Make cards fill the usable height dynamically
    usable = H - BOTTOM - TOP
    label_h_est = 30 if label else 0
    headline_h_est = measure_headline(draw, lines, 46)
    available_for_grid = usable - label_h_est - 16 - headline_h_est - 24
    card_h = max(200, (available_for_grid - 20) // 2)
    grid_h = card_h * 2 + 20

    label_h = 30 if label else 0
    headline_h = measure_headline(draw, lines, 46)
    total_h = label_h + 16 + headline_h + 24 + grid_h

    # Center within usable area (between header and bottom padding)
    usable_top = TOP
    usable_bottom = H - BOTTOM
    center_y = usable_top + (usable_bottom - usable_top - total_h) // 2
    y = max(usable_top, center_y)

    if label:
        y = draw_label(draw, label, y=y, theme=theme) + 16

    highlights = s.get("headline_highlight", [False] * len(lines))
    y = draw_headline(draw, lines, highlights, y, size=46, theme=theme)
    y += 24

    f_num = font("Bold", 52)
    f_lbl = font("Regular", 20)

    positions = [
        (PAD, y),                      (PAD + card_w + 24, y),
        (PAD, y + card_h + 20),        (PAD + card_w + 24, y + card_h + 20),
    ]

    for i, item in enumerate(items):
        if i >= len(positions):
            break
        x, cy = positions[i]
        rounded_rect(draw, [x, cy, x + card_w, cy + card_h], 16,
                     fill=card_fill(theme), outline=card_border(theme))
        n_color = rgb(COLOR_NAMES.get(item.get("color", "blue"), C["blue"]))
        n_text = item.get("number", "")
        nx = x + (card_w - (draw.textbbox((0, 0), n_text, font=f_num)[2])) // 2
        draw.text((nx, cy + 26), n_text, fill=n_color, font=f_num)
        for j, lline in enumerate(item.get("label", "").split("\n")):
            lx = x + (card_w - (draw.textbbox((0, 0), lline, font=f_lbl)[2])) // 2
            draw.text((lx, cy + 122 + j * 28), lline, fill=fg_secondary(theme), font=f_lbl)


def render_checklist(draw, s, num, total, theme="dark"):
    label = s.get("label", "")
    lines = s.get("headline", [])
    items = s.get("items", [])

    row_h = 88
    gap = 14
    label_h = 30 if label else 0
    headline_h = measure_headline(draw, lines, 46)
    list_h = len(items) * (row_h + gap) - gap
    total_h = label_h + 16 + headline_h + 16 + list_h

    usable = H - BOTTOM - TOP
    y = max(TOP, TOP + (usable - total_h) // 2)

    if label:
        y = draw_label(draw, label, y=y, theme=theme) + 16

    highlights = s.get("headline_highlight", [False] * len(lines))
    y = draw_headline(draw, lines, highlights, y, size=46, theme=theme)
    y += 16

    f_name = font("Bold", 24)
    f_detail = font("Regular", 20)

    for item in items:
        if y + row_h > H - BOTTOM:
            break
        rounded_rect(draw, [PAD, y, W - PAD, y + row_h], 12,
                     fill=card_fill(theme), outline=card_border(theme))
        cx2, cy2 = PAD + 40, y + row_h // 2
        draw.line([(cx2 - 10, cy2), (cx2 - 2, cy2 + 9), (cx2 + 10, cy2 - 10)],
                  fill=rgb(C["blue"]), width=3)
        draw.text((PAD + 64, y + 18), item.get("name", ""), fill=fg_color(theme), font=f_name)
        detail = item.get("detail", "")
        if detail:
            d_x = PAD + 64 + draw.textbbox((0, 0), item.get("name", "") + "   ", font=f_name)[2]
            draw.text((d_x, y + 22), detail, fill=fg_muted(theme), font=f_detail)
        y += row_h + gap


def render_timeline(draw, s, num, total, theme="dark"):
    label = s.get("label", "")
    lines = s.get("headline", [])
    subtitle = s.get("subtitle", "")
    events = s.get("events", [])

    label_h = 30 if label else 0
    headline_h = measure_headline(draw, lines, 46)
    subtitle_h = 40 if subtitle else 0
    event_h = min(130, (H - BOTTOM - TOP - label_h - 16 - headline_h - subtitle_h - 28) // max(len(events), 1))
    timeline_h = len(events) * event_h

    total_h = label_h + 16 + headline_h + subtitle_h + 28 + timeline_h
    usable = H - BOTTOM - TOP
    y = max(TOP, TOP + (usable - total_h) // 2)

    if label:
        y = draw_label(draw, label, y=y, theme=theme) + 16

    highlights = s.get("headline_highlight", [False] * len(lines))
    y = draw_headline(draw, lines, highlights, y, size=46, theme=theme)

    if subtitle:
        y += 6
        draw_wrapped_centered(draw, subtitle, font("Regular", 20), fg_muted(theme), y)
    y += 28

    line_x = PAD + 10
    f_date = font("Bold", 17)
    f_title = font("Bold", 22)
    f_desc = font("Regular", 19)
    dot_colors = [rgb(C["blue"]), rgb(C["lilac"]), rgb(C["violet"]), rgb(C["violet"])]

    for i, ev in enumerate(events):
        ey = y + i * event_h
        if i < len(events) - 1:
            t0 = i / (len(events) - 1) if len(events) > 1 else 0
            t1 = (i + 1) / (len(events) - 1) if len(events) > 1 else 1
            for yy in range(ey, ey + event_h):
                t = t0 + (yy - ey) / event_h * (t1 - t0)
                c = lerp_color(rgb(C["blue"]), rgb(C["violet"]), t)
                draw.point((line_x, yy), fill=c)
                draw.point((line_x + 1, yy), fill=c)

        dc = dot_colors[i % len(dot_colors)]
        draw.ellipse([line_x - 6, ey - 6, line_x + 8, ey + 8], fill=dc)

        tx = line_x + 28
        draw.text((tx, ey - 10), ev.get("date", ""), fill=fg_muted(theme), font=f_date)
        draw.text((tx, ey + 14), ev.get("title", ""), fill=fg_color(theme), font=f_title)
        if ev.get("desc"):
            draw.text((tx, ey + 44), ev["desc"], fill=fg_secondary(theme), font=f_desc)


def render_cards(draw, s, num, total, theme="dark"):
    label = s.get("label", "")
    lines = s.get("headline", [])
    items = s.get("items", [])

    card_h = 148
    gap = 22
    label_h = 30 if label else 0
    headline_h = measure_headline(draw, lines, 46)
    cards_h = len(items) * (card_h + gap) - gap
    total_h = label_h + 16 + headline_h + 12 + cards_h

    usable = H - BOTTOM - TOP
    y = max(TOP, TOP + (usable - total_h) // 2)

    if label:
        y = draw_label(draw, label, y=y, theme=theme) + 16

    highlights = s.get("headline_highlight", [False] * len(lines))
    hc = s.get("headline_color", "pink")
    y = draw_headline(draw, lines, highlights, y, size=46, highlight_color=hc, theme=theme)
    y += 12

    f_num = font("Bold", 38)
    f_title = font("Bold", 23)
    f_desc = font("Regular", 20)

    for item in items:
        if y + card_h > H - BOTTOM:
            break
        rounded_rect(draw, [PAD, y, W - PAD, y + card_h], 16,
                     fill=card_fill(theme), outline=card_border(theme))
        draw.text((PAD + 28, y + 20), item.get("number", ""), fill=rgb(C["pink"]), font=f_num)
        draw.text((PAD + 90, y + 22), item.get("title", ""), fill=fg_color(theme), font=f_title)
        desc = item.get("desc", "")
        if desc:
            draw_wrapped_centered(draw, desc, f_desc, fg_secondary(theme),
                                  y + 70, W - PAD * 2 - 40)
        y += card_h + gap


def render_cta(draw, img, s, num, total, theme="dark"):
    draw_glow(img, alpha=12, radius=300, theme=theme)
    draw = ImageDraw.Draw(img)
    _draw_gradient_bar(draw)

    lines = s.get("headline", [])
    taglines = s.get("taglines", [])
    btn_text = s.get("cta_button", "Follow for more")
    author = s.get("author", "")

    headline_h = measure_headline(draw, lines, 64)
    taglines_h = len(taglines) * 40
    approx_h = headline_h + 12 + taglines_h + 24 + 64 + (40 if author else 0)
    y = max(TOP + 20, (H - approx_h) // 2)

    highlights = s.get("headline_highlight", [False] * len(lines))
    y = draw_headline(draw, lines, highlights, y, size=64, theme=theme)
    y += 12

    for tl in taglines:
        y = draw_centered(draw, y, tl, font("Regular", 23), fg_secondary(theme)) + 10
    y += 24

    f_cta = font("Bold", 24)
    btn_bbox = draw.textbbox((0, 0), btn_text, font=f_cta)
    btn_tw = btn_bbox[2] - btn_bbox[0]
    btn_w = btn_tw + 80
    btn_h = 64
    btn_x = (W - btn_w) // 2
    rounded_rect(draw, [btn_x, y, btn_x + btn_w, y + btn_h], 16, fill=rgb(C["blue"]))
    tx = btn_x + (btn_w - btn_tw) // 2
    draw.text((tx, y + (btn_h - 28) // 2), btn_text, fill=rgb(C["white"]), font=f_cta)
    y += btn_h + 28

    if author:
        draw_centered(draw, y, author, font("Medium", 20), fg_muted(theme))


# ── Dispatch ───────────────────────────────────────────────────────────────────

RENDERERS = {
    "title":     render_title,
    "stat":      render_stat,
    "text":      render_text,
    "grid":      render_grid,
    "checklist": render_checklist,
    "timeline":  render_timeline,
    "cards":     render_cards,
    "cta":       render_cta,
}


def render_slide(slide_spec, num, total, out_dir):
    stype = slide_spec.get("type", "text")

    # Theme assignment: title + CTA always dark; content slides alternate dark/light
    if stype in ("title", "cta"):
        theme = "dark"
    else:
        theme = "dark" if num % 2 == 1 else "light"

    img, draw = new_slide(theme=theme)

    renderer = RENDERERS.get(stype)
    if renderer is None:
        print(f"  Warning: unknown slide type '{stype}', skipping", file=sys.stderr)
        return

    if stype in ("title", "cta"):
        renderer(draw, img, slide_spec, num, total, theme=theme)
    else:
        renderer(draw, slide_spec, num, total, theme=theme)

    # Re-draw chrome on top (gradient bar, logo, slide number)
    draw = ImageDraw.Draw(img)
    _draw_gradient_bar(draw)
    add_logo(img, draw, theme=theme)
    add_slide_number(draw, num, total, theme=theme)

    fname = f"slide_{num:02d}.png"
    fpath = os.path.join(out_dir, fname)
    img.save(fpath, "PNG")
    print(f"  ✓ {fname}")
    return fpath


def main():
    parser = argparse.ArgumentParser(description="Generate Amplitude LinkedIn carousel PNGs")
    parser.add_argument("--slides", help="JSON array of slide specs (inline)")
    parser.add_argument("--slides-file", help="Path to JSON file with slide specs")
    parser.add_argument("--output", required=True, help="Output directory for PNGs")
    args = parser.parse_args()

    if args.slides_file:
        with open(args.slides_file) as f:
            slides = json.load(f)
    elif args.slides:
        slides = json.loads(args.slides)
    else:
        print("Error: provide --slides or --slides-file", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)
    total = len(slides)
    print(f"Generating {total} slides → {args.output}/")

    for i, slide in enumerate(slides, 1):
        render_slide(slide, i, total, args.output)

    print(f"\nDone! {total} slides saved.")


if __name__ == "__main__":
    main()
