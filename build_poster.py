#!/usr/bin/env python3
"""Draw the 22 November 2026 news poster as a 1024x1024 PNG.

The picture is a dark-navy front page: a masthead naming the day,
one lead panel about NATO and Poland, four story cards in a
two-by-two grid, a full-width card on a pair of hacking stories,
and a short ALSO TODAY strip along the bottom.

Everything is drawn with fixed coordinates and the DejaVu fonts, so
running this script again always produces the same image bytes.
The layout keeps the previous days' front-page shape, tightened a
little so the longer ALSO TODAY strip still fits above the footer.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
MARGIN = 36
CONTENT = WIDTH - 2 * MARGIN

BACKGROUND = (9, 20, 38)
PANEL = (16, 33, 57)
PANEL_ALT = (20, 39, 66)
GOLD = (216, 178, 62)
PAPER = (236, 241, 248)
MUTED = (168, 184, 204)
ACCENT = (232, 92, 82)
TEAL = (84, 196, 178)

BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

HERE = Path(__file__).resolve().parent


def font(size, bold=False):
    """Load one DejaVu face at the requested pixel size."""
    return ImageFont.truetype(BOLD_PATH if bold else PLAIN_PATH, size)


def wrap_lines(draw, text, face, limit):
    """Split text into lines that each fit inside limit pixels."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        box = draw.textbbox((0, 0), trial, font=face)
        if box[2] - box[0] <= limit or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, face, fill, limit, leading):
    """Draw wrapped text from xy and return the y just past it."""
    x, y = xy
    for line in wrap_lines(draw, text, face, limit):
        draw.text((x, y), line, font=face, fill=fill)
        y += leading
    return y


def panel_box(draw, box, fill=PANEL):
    """Draw one rounded story panel with a thin outline."""
    draw.rounded_rectangle(box, radius=14, fill=fill, outline=(52, 76, 108), width=2)


def card(draw, box, kicker, headline, body, accent=GOLD):
    """Fill one grid card with a kicker, a headline and body copy."""
    panel_box(draw, box, fill=PANEL_ALT)
    x0, y0, x1, _ = box
    inner = x1 - x0 - 32
    draw.rectangle([x0, y0 + 10, x0 + 5, y0 + 58], fill=accent)
    y = draw_wrapped(draw, (x0 + 16, y0 + 12), kicker, font(15, bold=True), accent, inner, 19)
    y = draw_wrapped(draw, (x0 + 16, y + 2), headline, font(21, bold=True), PAPER, inner, 25)
    draw_wrapped(draw, (x0 + 16, y + 4), body, font(16), MUTED, inner, 20)


def build_poster():
    """Render the whole front page and save it beside this script."""
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    # Masthead: the title, then the day it sums up in gold.
    title_face = font(43, bold=True)
    title = "THE WORLD IN ONE IMAGE"
    title_box = draw.textbbox((0, 0), title, font=title_face)
    title_w = title_box[2] - title_box[0]
    draw.text(((WIDTH - title_w) / 2, 24), title, font=title_face, fill=PAPER)
    date_face = font(22, bold=True)
    date_text = "SUNDAY · 22 NOVEMBER 2026"
    date_box = draw.textbbox((0, 0), date_text, font=date_face)
    date_w = date_box[2] - date_box[0]
    draw.text(((WIDTH - date_w) / 2, 78), date_text, font=date_face, fill=GOLD)
    draw.rectangle([MARGIN, 116, WIDTH - MARGIN, 120], fill=GOLD)

    # Lead panel: NATO vows to defend Poland after the violation.
    lead_box = [MARGIN, 132, WIDTH - MARGIN, 382]
    panel_box(draw, lead_box)
    draw.rectangle([MARGIN, 142, MARGIN + 5, 196], fill=ACCENT)
    y = draw_wrapped(draw, (MARGIN + 20, 146), "LEAD · NATO AND UKRAINE",
                     font(16, bold=True), ACCENT, CONTENT - 40, 20)
    y = draw_wrapped(draw, (MARGIN + 20, y + 4), "NATO VOWS TO DEFEND POLAND",
                     font(35, bold=True), PAPER, CONTENT - 40, 42)
    lead_body = (
        "NATO vows to defend \"every inch\" of Polish territory after a "
        "Russian airspace violation. Russia strikes Zelenskyy's hometown "
        "Kryvyi Rih, killing an emergency worker and a 7-year-old boy. "
        "Ukraine marks the Day of Dignity and Freedom and keeps hitting "
        "the Crimean Bridge; Zelenskyy brands Putin a \"killer\" after "
        "Trump calls him his \"friend\"."
    )
    draw_wrapped(draw, (MARGIN + 20, y + 8), lead_body, font(19), MUTED,
                 CONTENT - 40, 26)

    # Two-by-two grid of the next four stories.
    gap = 14
    card_w = (CONTENT - gap) // 2
    card_h = 164
    top_row = 396
    bottom_row = top_row + card_h + gap
    left_x = MARGIN
    right_x = MARGIN + card_w + gap
    card(draw, [left_x, top_row, left_x + card_w, top_row + card_h],
         "MIDDLE EAST · HORMUZ", "HORMUZ",
         "Bahrain says Iran struck an industrial site as tankers are hit "
         "in the Strait of Hormuz. Iran: a reopening is possible if the "
         "US accepts \"reasonable\" terms. Pentagon: war cost over "
         "$48 billion.")
    card(draw, [right_x, top_row, right_x + card_w, top_row + card_h],
         "MEXICO · CARTEL ARREST", "EL CHAPO ISIDRO",
         "Mexico captures FBI Ten Most Wanted cartel boss \"El Chapo "
         "Isidro\" with US support. Deadly Sinaloa violence leaves 11 "
         "dead after the arrest.", accent=TEAL)
    card(draw, [left_x, bottom_row, left_x + card_w, bottom_row + card_h],
         "CLIMATE · COP31", "COP31",
         "Climate talks stretch into overtime with no agreement in "
         "sight — the fossil-fuel dispute threatens to scupper the deal "
         "as countries remain divided on key issues.", accent=TEAL)
    card(draw, [right_x, bottom_row, right_x + card_w, bottom_row + card_h],
         "UNITED STATES · TRUMP", "TRUMP CAP",
         "Trump vows to work with Democrats to cap credit card interest "
         "rates at 10%.")

    # Full-width card: breaches and a probe, side by side.
    wide_top = bottom_row + card_h + gap
    wide_box = [MARGIN, wide_top, WIDTH - MARGIN, wide_top + 112]
    panel_box(draw, wide_box)
    draw.rectangle([MARGIN, wide_top + 10, MARGIN + 5, wide_top + 58], fill=GOLD)
    y = draw_wrapped(draw, (MARGIN + 20, wide_top + 12), "SECURITY AND TECH · UNITED STATES",
                     font(15, bold=True), GOLD, CONTENT - 40, 19)
    y = draw_wrapped(draw, (MARGIN + 20, y + 2), "HACKED",
                     font(21, bold=True), PAPER, CONTENT - 40, 25)
    wide_body = (
        "The US Agriculture Department and the FBI are breached by hackers, "
        "reports say; Nvidia faces a US accounting probe as Jensen Huang's "
        "exit and a China spy saga deepen the turmoil."
    )
    draw_wrapped(draw, (MARGIN + 20, y + 4), wide_body, font(16), MUTED,
                 CONTENT - 40, 21)

    # Closing strip with the rest of the day in brief.
    strip_top = wide_top + 120
    draw.rectangle([MARGIN, strip_top, WIDTH - MARGIN, strip_top + 3], fill=GOLD)
    y = draw_wrapped(draw, (MARGIN, strip_top + 12), "ALSO TODAY",
                     font(17, bold=True), GOLD, CONTENT, 21)
    also_body = (
        "Fire at a Jakarta confectionery factory kills three, 36 missing · "
        "At least 24 dead in Nigeria when a boat capsizes carrying people "
        "to a funeral · French protesters rally for a sixth weekend over "
        "living costs · China opposes the US ban on telecom firms' access "
        "to phone numbers."
    )
    draw_wrapped(draw, (MARGIN, y + 4), also_body, font(16), PAPER, CONTENT, 21)

    # Small edition line so the page reads as one finished front page.
    foot_face = font(13)
    foot_text = "Wire reports of 22 November 2026 · One page, one day"
    foot_box = draw.textbbox((0, 0), foot_text, font=foot_face)
    foot_w = foot_box[2] - foot_box[0]
    draw.text(((WIDTH - foot_w) / 2, 992), foot_text, font=foot_face, fill=MUTED)

    target = HERE / "entry.png"
    image.save(target, format="PNG")
    return target


if __name__ == "__main__":
    print(build_poster())
