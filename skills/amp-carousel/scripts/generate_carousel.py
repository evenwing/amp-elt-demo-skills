#!/usr/bin/env python3
"""
Amplitude LinkedIn Carousel Generator
Generates 1080x1080 PNG slides from a JSON slide spec.

Usage:
  python3 generate_carousel.py --slides '<JSON array>' --output /path/to/output/dir
  python3 generate_carousel.py --slides-file slides.json --output /path/to/output/dir
  python3 generate_carousel.py --slides-file slides.json --output /out --logo-dir '/path/to/Amplitude Logo'
"""

import argparse
import json
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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


# ── Logo cache ───────────────────────────────────────────────────────────────
_LOGO_CACHE = {}


def _load_logo(logo_dir):
    """Load and cache the Amplitude logo for compositing onto slides."""
    if "full" in _LOGO_CACHE:
        return _LOGO_CACHE["full"]

    full_path = os.path.join(logo_dir, "Full", "PNG (RGB)",
                             "logo_amplitude_full_blue_RGB.png")
    full_img = None

    if os.path.exists(full_path):
        full_img = Image.open(full_path).convert("RGBA")
        # Scale to 44px height to match logo area
        scale = 44 / full_img.height
        full_img = full_img.resize((int(full_img.width * scale), 44), Image.LANCZOS)

    _LOGO_CACHE["full"] = full_img
    return full_img


# ── Base slide setup ──────────────────────────────────────────────────────────

def new_slide():
    img = Image.new("RGB", (W, H), rgb(C["black"]))
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


def add_logo(draw, img=None, logo_dir=None):
    """Paste the real Amplitude logo PNG, or fall back to a drawn version."""
    logo_img = None
    if logo_dir:
        logo_img = _load_logo(logo_dir)

    if logo_img and img:
        img.paste(logo_img, (PAD, 38), logo_img)
    else:
        # Fallback: drawn logo mark + wordmark
        draw.rounded_rectangle([PAD, 38, PAD + 44, 82], radius=10, fill=rgb(C["blue"]))
        draw.text((PAD + 10, 43), "A", fill=rgb(C["white"]), font=font("Bold", 24))
        draw.text((PAD + 56, 48), "Amplitude", fill=rgb(C["g40"]), font=font("Bold", 20))


def add_slide_number(draw, num, total):
    f = font("Medium", 18)
    text = f"{num} / {total}"
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text((W - PAD - tw, 52), text, fill=rgb(C["g70"]), font=f)


# ── Layout helpers ─────────────────────────────────────────────────────────────

def center_x(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return (W - (bbox[2] - bbox[0])) // 2


def draw_centered(draw, y, text, fnt, color):
    x = center_x(draw, text, fnt)
    draw.text((x, y), text, fill=color, font=fnt)
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return y + (bbox[3] - bbox[1])


def draw_label(draw, text, y=TOP):
    f = font("Bold", 18)
    cx = center_x(draw, text, f)
    draw.text((cx, y), text, fill=rgb(C["blue"]), font=f)
    return y + 30


def draw_headline(draw, lines, highlights, y, size=48, highlight_color="blue"):
    f = font("Bold", size)
    hc = rgb(COLOR_NAMES.get(highlight_color, C["blue"]))
    for i, line in enumerate(lines):
        color = hc if (i < len(highlights) and highlights[i]) else rgb(C["white"])
        y = draw_centered(draw, y, line, f, color) + 8
    return y + 8


def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_glow(img, alpha=12, radius=280):
    """Subtle blue center glow."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(radius, 0, -1):
        a = int(alpha * (r / radius))
        gd.ellipse([W//2 - r, H//2 - r, W//2 + r, H//2 + r], fill=(0, 82, 242, a))
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    merged = Image.alpha_composite(base, glow).convert("RGB")
    img.paste(merged)


def draw_wave_motif(img, y_center=540, amplitude=120, waves=2.5, thickness=60):
    """Draw an abstract extruded wave ribbon inspired by Amplitude's brand
    graphic elements. Creates a flowing 3D-style wave with blue-violet gradient."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Multiple offset layers for a 3D extruded ribbon effect (back to front)
    layers = [
        (18, 0.15, rgb(C["violet"])),
        (10, 0.25, rgb(C["lilac"])),
        (0, 0.45, rgb(C["blue"])),
    ]

    for y_off, alpha_mult, base_color in layers:
        for x in range(W):
            t = x / W
            wave_y = y_center + y_off + int(amplitude * math.sin(t * waves * 2 * math.pi + 0.5))
            # Gradient color along x
            tc = min(1.0, t * 1.2)
            r = int(base_color[0] + (rgb(C["violet"])[0] - base_color[0]) * tc)
            g = int(base_color[1] + (rgb(C["violet"])[1] - base_color[1]) * tc)
            b = int(base_color[2] + (rgb(C["violet"])[2] - base_color[2]) * tc)

            half_t = thickness // 2
            for dy in range(-half_t, half_t):
                edge_dist = abs(dy) / half_t
                a = int(255 * alpha_mult * (1 - edge_dist ** 1.5))
                if a > 0:
                    fy = wave_y + dy
                    if 0 <= fy < H:
                        od.point((x, fy), fill=(r, g, b, a))

    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=3))

    base = img.convert("RGBA")
    composited = Image.alpha_composite(base, overlay).convert("RGB")
    img.paste(composited)


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


# ── Slide renderers ────────────────────────────────────────────────────────────

def render_title(draw, img, s, num, total, logo_dir=None):
    draw_glow(img, alpha=14, radius=300)
    draw_wave_motif(img, y_center=720, amplitude=80, waves=1.8, thickness=50)
    draw = ImageDraw.Draw(img)
    _draw_gradient_bar(draw)
    add_logo(draw, img=img, logo_dir=logo_dir)
    add_slide_number(draw, num, total)

    y = 260
    # Hook
    hook = s.get("hook", "")
    if hook:
        f_hook = font("Bold", 18)
        cx = center_x(draw, hook, f_hook)
        draw.text((cx, y), hook, fill=rgb(C["blue"]), font=f_hook)
        y += 36

    # Headline
    lines = s.get("headline", [])
    highlights = s.get("headline_highlight", [False] * len(lines))
    f_h = font("Bold", 72)
    for i, line in enumerate(lines):
        color = rgb(C["blue"]) if (i < len(highlights) and highlights[i]) else rgb(C["white"])
        y = draw_centered(draw, y, line, f_h, color) + 10
    y += 16

    # Subtitle
    subtitle = s.get("subtitle", "")
    if subtitle:
        draw_wrapped_centered(draw, subtitle, font("Regular", 24), rgb(C["g40"]), y, W - 200)

    # Swipe
    if s.get("swipe", True):
        f_sw = font("Medium", 17)
        draw_centered(draw, H - 68, "SWIPE →", f_sw, rgb(C["g70"]))


def render_stat(draw, img, s, num, total, logo_dir=None):
    add_logo(draw, img=img, logo_dir=logo_dir)
    add_slide_number(draw, num, total)

    # Estimate total content height then center vertically
    ctx_lines = s.get("context", [])
    approx_h = 170 + 50 + 40 + 60 + len(ctx_lines) * 60
    y = max(TOP, (H - approx_h) // 2)

    label = s.get("label", "")
    if label:
        y = draw_label(draw, label, y=y) + 16

    # Big number
    big = s.get("big_number", "")
    f_big = font("Bold", 160)
    draw_centered(draw, y, big, f_big, rgb(C["blue"]))
    y += 180

    unit = s.get("big_unit", "")
    if unit:
        y = draw_centered(draw, y, unit, font("Bold", 36), rgb(C["lilac"])) + 12

    date = s.get("date", "")
    if date:
        y = draw_centered(draw, y, date, font("Medium", 24), rgb(C["g20"])) + 32

    # Divider
    draw.line([(PAD + 80, y), (W - PAD - 80, y)], fill=rgb(C["g90"]), width=1)
    y += 28

    # FIX: use return value of draw_wrapped_centered to avoid text overlap
    for i, line in enumerate(ctx_lines):
        fnt = font("Bold", 20) if i == len(ctx_lines) - 1 else font("Regular", 20)
        clr = rgb(C["g40"]) if i == len(ctx_lines) - 1 else rgb(C["g60"])
        y = draw_wrapped_centered(draw, line, fnt, clr, y, W - PAD * 2 - 80, line_gap=8)
        y += 12


def render_text(draw, img, s, num, total, logo_dir=None):
    add_logo(draw, img=img, logo_dir=logo_dir)
    add_slide_number(draw, num, total)

    lines = s.get("headline", [])
    body = s.get("body", "")
    callout = s.get("callout", "")
    # Estimate height for vertical centering
    approx_h = 30 + len(lines) * 62 + (90 if body else 0) + (130 if callout else 0)
    y = max(TOP, (H - approx_h) // 2)

    label = s.get("label", "")
    if label:
        y = draw_label(draw, label, y=y) + 16

    highlights = s.get("headline_highlight", [False] * len(lines))
    y = draw_headline(draw, lines, highlights, y, size=46)
    y += 16

    if body:
        y = draw_wrapped_centered(draw, body, font("Regular", 26), rgb(C["g30"]), y, W - 160, line_gap=14)

    if callout:
        y += 28
        box_h = 100
        rounded_rect(draw, [PAD, y, W - PAD, y + box_h], 16,
                     fill=rgb(C["g100"]), outline=rgb(C["g90"]))
        draw_wrapped_centered(draw, callout, font("Medium", 22), rgb(C["white"]),
                              y + (box_h - 28) // 2, W - PAD * 2 - 60)


def render_grid(draw, img, s, num, total, logo_dir=None):
    add_logo(draw, img=img, logo_dir=logo_dir)
    add_slide_number(draw, num, total)

    y = draw_label(draw, s.get("label", ""), y=TOP)
    y += 12

    lines = s.get("headline", [])
    highlights = s.get("headline_highlight", [False] * len(lines))
    y = draw_headline(draw, lines, highlights, y, size=46)
    y += 16

    items = s.get("items", [])[:4]
    card_w = (W - PAD * 2 - 24) // 2
    card_h = 185
    f_num = font("Bold", 52)
    f_lbl = font("Regular", 20)

    positions = [
        (PAD, y), (PAD + card_w + 24, y),
        (PAD, y + card_h + 20), (PAD + card_w + 24, y + card_h + 20),
    ]

    for i, item in enumerate(items):
        if i >= len(positions):
            break
        x, cy = positions[i]
        rounded_rect(draw, [x, cy, x + card_w, cy + card_h], 16,
                     fill=rgb(C["g100"]), outline=rgb(C["g90"]))
        n_color = rgb(COLOR_NAMES.get(item.get("color", "blue"), C["blue"]))
        n_text = item.get("number", "")
        nx = x + (card_w - (draw.textbbox((0, 0), n_text, font=f_num)[2])) // 2
        draw.text((nx, cy + 20), n_text, fill=n_color, font=f_num)
        for j, lline in enumerate(item.get("label", "").split("\n")):
            lx = x + (card_w - (draw.textbbox((0, 0), lline, font=f_lbl)[2])) // 2
            draw.text((lx, cy + 108 + j * 28), lline, fill=rgb(C["g40"]), font=f_lbl)


def render_checklist(draw, img, s, num, total, logo_dir=None):
    add_logo(draw, img=img, logo_dir=logo_dir)
    add_slide_number(draw, num, total)

    lines = s.get("headline", [])
    items = s.get("items", [])
    row_h = 80
    row_gap = 14

    # FIX: vertical centering — estimate total content height
    approx_h = 30 + len(lines) * 62 + 16 + len(items) * (row_h + row_gap)
    y = max(TOP, (H - approx_h) // 2)

    y = draw_label(draw, s.get("label", ""), y=y)
    y += 12

    highlights = s.get("headline_highlight", [False] * len(lines))
    y = draw_headline(draw, lines, highlights, y, size=46)
    y += 16

    f_name = font("Bold", 24)
    f_detail = font("Regular", 20)

    for item in items:
        if y + row_h > H - BOTTOM:
            break
        rounded_rect(draw, [PAD, y, W - PAD, y + row_h], 12,
                     fill=rgb(C["g100"]), outline=rgb(C["g90"]))
        cx2, cy2 = PAD + 40, y + row_h // 2
        draw.line([(cx2 - 10, cy2), (cx2 - 2, cy2 + 9), (cx2 + 10, cy2 - 10)],
                  fill=rgb(C["blue"]), width=3)
        draw.text((PAD + 64, y + 14), item.get("name", ""), fill=rgb(C["white"]), font=f_name)
        detail = item.get("detail", "")
        if detail:
            d_x = PAD + 64 + draw.textbbox((0, 0), item.get("name", "") + "   ", font=f_name)[2]
            draw.text((d_x, y + 18), detail, fill=rgb(C["g50"]), font=f_detail)
        y += row_h + row_gap


def render_timeline(draw, img, s, num, total, logo_dir=None):
    add_logo(draw, img=img, logo_dir=logo_dir)
    add_slide_number(draw, num, total)

    y = draw_label(draw, s.get("label", ""), y=TOP)
    y += 12

    lines = s.get("headline", [])
    highlights = s.get("headline_highlight", [False] * len(lines))
    y = draw_headline(draw, lines, highlights, y, size=46)

    subtitle = s.get("subtitle", "")
    if subtitle:
        y += 6
        draw_wrapped_centered(draw, subtitle, font("Regular", 20), rgb(C["g50"]), y)
    y += 28

    events = s.get("events", [])
    line_x = PAD + 10
    event_h = (H - BOTTOM - y) // max(len(events), 1)
    event_h = min(event_h, 130)

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
        draw.text((tx, ey - 10), ev.get("date", ""), fill=rgb(C["g60"]), font=f_date)
        draw.text((tx, ey + 14), ev.get("title", ""), fill=rgb(C["white"]), font=f_title)
        if ev.get("desc"):
            draw.text((tx, ey + 44), ev["desc"], fill=rgb(C["g40"]), font=f_desc)


def render_cards(draw, img, s, num, total, logo_dir=None):
    add_logo(draw, img=img, logo_dir=logo_dir)
    add_slide_number(draw, num, total)

    lines = s.get("headline", [])
    items = s.get("items", [])
    card_h = 148
    card_gap = 22

    # FIX: vertical centering — estimate total content height
    approx_h = 30 + len(lines) * 62 + 12 + len(items) * (card_h + card_gap)
    y = max(TOP, (H - approx_h) // 2)

    y = draw_label(draw, s.get("label", ""), y=y)
    y += 12

    highlights = s.get("headline_highlight", [False] * len(lines))
    hc = s.get("headline_color", "pink")
    y = draw_headline(draw, lines, highlights, y, size=46, highlight_color=hc)
    y += 12

    f_num = font("Bold", 38)
    f_title = font("Bold", 23)
    f_desc = font("Regular", 20)

    for item in items:
        if y + card_h > H - BOTTOM:
            break
        rounded_rect(draw, [PAD, y, W - PAD, y + card_h], 16,
                     fill=rgb(C["g100"]), outline=rgb(C["g90"]))
        draw.text((PAD + 28, y + 20), item.get("number", ""), fill=rgb(C["pink"]), font=f_num)
        draw.text((PAD + 90, y + 22), item.get("title", ""), fill=rgb(C["white"]), font=f_title)
        desc = item.get("desc", "")
        if desc:
            draw_wrapped_centered(draw, desc, f_desc, rgb(C["g40"]),
                                  y + 66, W - PAD * 2 - 40)
        y += card_h + card_gap


def render_cta(draw, img, s, num, total, logo_dir=None):
    draw_glow(img, alpha=12, radius=300)
    draw = ImageDraw.Draw(img)
    _draw_gradient_bar(draw)
    add_logo(draw, img=img, logo_dir=logo_dir)
    add_slide_number(draw, num, total)

    y = 300
    lines = s.get("headline", [])
    highlights = s.get("headline_highlight", [False] * len(lines))
    y = draw_headline(draw, lines, highlights, y, size=64)
    y += 12

    taglines = s.get("taglines", [])
    for tl in taglines:
        y = draw_centered(draw, y, tl, font("Regular", 23), rgb(C["g40"])) + 10
    y += 24

    # CTA button
    btn_text = s.get("cta_button", "Follow for more")
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

    author = s.get("author", "")
    if author:
        draw_centered(draw, y, author, font("Medium", 20), rgb(C["g60"]))


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


def render_slide(slide_spec, num, total, out_dir, logo_dir=None):
    img, draw = new_slide()
    stype = slide_spec.get("type", "text")
    renderer = RENDERERS.get(stype)

    if renderer is None:
        print(f"  Warning: unknown slide type '{stype}', skipping", file=sys.stderr)
        return

    # All renderers take uniform signature: (draw, img, spec, num, total, logo_dir)
    renderer(draw, img, slide_spec, num, total, logo_dir=logo_dir)

    # Re-draw logo/number after any overlay effects (glow, wave)
    draw = ImageDraw.Draw(img)
    add_logo(draw, img=img, logo_dir=logo_dir)
    add_slide_number(draw, num, total)

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
    parser.add_argument("--logo-dir",
                        help="Path to 'Amplitude Logo' directory (contains Full/, Mark/ subdirs)")
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

    logo_dir = args.logo_dir
    for i, slide in enumerate(slides, 1):
        render_slide(slide, i, total, args.output, logo_dir=logo_dir)

    print(f"\nDone! {total} slides saved.")


if __name__ == "__main__":
    main()
