#!/usr/bin/env python3
"""Compose the Sunday 22 November 2026 world-news poster.

Rather than placing every story at a hand-picked coordinate, this
renderer treats the page as a vertical stack of sections.  A small
catalogue below describes each story once; the renderer then walks
that catalogue from top to bottom, giving the lead a tall slot, the
four middle stories two paired rows, the hacking story a wide slot,
and the short items a closing text block.  Pillow supplies the
canvas and the DejaVu typefaces supply the lettering.
Section heights are fixed allocations in the walk, chosen so the
longest stories of the day still land inside their boxes.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
EDGE = 40
SPAN = PAGE - EDGE * 2
GUTTER = 12

INK = (8, 18, 34)
BOX = (18, 36, 60)
BOX_SOFT = (22, 42, 68)
LINE = (58, 84, 118)
WHITE = (238, 243, 250)
GREY = (172, 188, 208)
YELLOW = (219, 181, 66)
RED = (233, 96, 84)
MINT = (86, 199, 181)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
HEAVY_FILE = FONT_DIR / "DejaVuSans-Bold.ttf"
LIGHT_FILE = FONT_DIR / "DejaVuSans.ttf"

OUTPUT_FILE = Path(__file__).resolve().parent / "entry.png"

LEAD_STORY = {
    "tag": "LEAD - NATO AND UKRAINE",
    "title": "NATO VOWS TO DEFEND POLAND",
    "text": (
        "NATO vows to defend every inch of Polish territory after a "
        "Russian airspace violation. Russia strikes Zelenskyy's "
        "hometown Kryvyi Rih, killing an emergency worker and a "
        "7-year-old boy. Ukraine marks the Day of Dignity and Freedom "
        "and keeps hitting the Crimean Bridge; Zelenskyy brands Putin "
        "a killer after Trump calls him his friend."
    ),
    "colour": RED,
}

GRID_STORIES = [
    {
        "tag": "MIDDLE EAST - HORMUZ",
        "title": "HORMUZ",
        "text": (
            "Bahrain says Iran struck an industrial site as tankers "
            "are hit in the Strait of Hormuz. Iran: a reopening is "
            "possible if the US accepts reasonable terms. Pentagon: "
            "war cost over $48 billion."
        ),
        "colour": YELLOW,
    },
    {
        "tag": "MEXICO - CARTEL ARREST",
        "title": "EL CHAPO ISIDRO",
        "text": (
            "Mexico captures FBI Ten Most Wanted cartel boss El Chapo "
            "Isidro with US support. Deadly Sinaloa violence leaves "
            "11 dead after the arrest."
        ),
        "colour": MINT,
    },
    {
        "tag": "CLIMATE - COP31",
        "title": "COP31",
        "text": (
            "Climate talks stretch into overtime with no agreement "
            "in sight - the fossil-fuel dispute threatens to scupper "
            "the deal as countries remain divided on key issues."
        ),
        "colour": MINT,
    },
    {
        "tag": "UNITED STATES - TRUMP",
        "title": "TRUMP CAP",
        "text": (
            "Trump vows to work with Democrats to cap credit card "
            "interest rates at 10%."
        ),
        "colour": YELLOW,
    },
]

WIDE_STORY = {
    "tag": "SECURITY AND TECH - UNITED STATES",
    "title": "HACKED",
    "text": (
        "The US Agriculture Department and the FBI are breached by "
        "hackers, reports say; Nvidia faces a US accounting probe as "
        "Jensen Huang's exit and a China spy saga deepen the turmoil."
    ),
    "colour": YELLOW,
}

BRIEF_ITEMS = [
    "Fire at a Jakarta confectionery factory kills three, 36 missing",
    "At least 24 dead in Nigeria when a boat capsizes carrying people to a funeral",
    "French protesters rally for a sixth weekend over living costs",
    "China opposes the US ban on telecom firms' access to phone numbers",
]


def typeface(points, heavy=False):
    """Return a DejaVu face, bold when heavy asks for weight."""
    chosen = HEAVY_FILE if heavy else LIGHT_FILE
    return ImageFont.truetype(str(chosen), points)


def break_into_lines(painter, wording, face, max_width):
    """Greedily pack words into lines no wider than max_width."""
    packed = []
    pending = ""
    for token in wording.split():
        attempt = token if pending == "" else pending + " " + token
        if painter.textlength(attempt, font=face) <= max_width or pending == "":
            pending = attempt
        else:
            packed.append(pending)
            pending = token
    if pending != "":
        packed.append(pending)
    return packed


def paint_text(painter, left, top, wording, face, colour, max_width, step):
    """Paint wording line by line and report the new vertical spot."""
    cursor = top
    for row in break_into_lines(painter, wording, face, max_width):
        painter.text((left, cursor), row, font=face, fill=colour)
        cursor += step
    return cursor


def paint_section(painter, rect, story, title_points=21):
    """Paint one boxed story: side stripe, tag, title, then body."""
    left, top, right, bottom = rect
    painter.rounded_rectangle(rect, radius=13, fill=BOX_SOFT, outline=LINE, width=2)
    painter.rectangle([left, top + 11, left + 5, top + 56], fill=story["colour"])
    inner_width = right - left - 34
    spot = paint_text(painter, left + 17, top + 12, story["tag"],
                      typeface(14, heavy=True), story["colour"], inner_width, 18)
    spot = paint_text(painter, left + 17, spot + 2, story["title"],
                      typeface(title_points, heavy=True), WHITE, inner_width, title_points + 4)
    paint_text(painter, left + 17, spot + 4, story["text"],
               typeface(15), GREY, inner_width, 20)


def paint_masthead(painter):
    """Paint the centred title block and return where stories begin."""
    banner = "THE WORLD IN ONE IMAGE"
    banner_face = typeface(42, heavy=True)
    banner_width = painter.textlength(banner, font=banner_face)
    painter.text(((PAGE - banner_width) / 2, 26), banner, font=banner_face, fill=WHITE)
    day = "SUNDAY - 22 NOVEMBER 2026"
    day_face = typeface(22, heavy=True)
    day_width = painter.textlength(day, font=day_face)
    painter.text(((PAGE - day_width) / 2, 80), day, font=day_face, fill=YELLOW)
    painter.rectangle([EDGE, 118, PAGE - EDGE, 122], fill=YELLOW)
    return 134


def render_page():
    """Assemble every section in order and save the finished page."""
    canvas = Image.new("RGB", (PAGE, PAGE), INK)
    painter = ImageDraw.Draw(canvas)
    cursor = paint_masthead(painter)

    # Lead slot: taller than the rest, with a larger title treatment.
    lead_rect = [EDGE, cursor, PAGE - EDGE, cursor + 232]
    painter.rounded_rectangle(lead_rect, radius=13, fill=BOX, outline=LINE, width=2)
    painter.rectangle([EDGE, cursor + 11, EDGE + 5, cursor + 62], fill=RED)
    lead_width = SPAN - 40
    spot = paint_text(painter, EDGE + 20, cursor + 14, LEAD_STORY["tag"],
                      typeface(16, heavy=True), RED, lead_width, 20)
    spot = paint_text(painter, EDGE + 20, spot + 4, LEAD_STORY["title"],
                      typeface(34, heavy=True), WHITE, lead_width, 41)
    paint_text(painter, EDGE + 20, spot + 8, LEAD_STORY["text"],
               typeface(18), GREY, lead_width, 25)
    cursor += 232 + GUTTER

    # Paired rows: the grid catalogue is consumed two stories at a time.
    column_width = (SPAN - GUTTER) // 2
    for pair_start in (0, 2):
        for offset in (0, 1):
            story = GRID_STORIES[pair_start + offset]
            col_left = EDGE + offset * (column_width + GUTTER)
            rect = [col_left, cursor, col_left + column_width, cursor + 158]
            paint_section(painter, rect, story)
        cursor += 158 + GUTTER

    # Wide slot for the hacking story, spanning the whole page width.
    wide_rect = [EDGE, cursor, PAGE - EDGE, cursor + 112]
    paint_section(painter, wide_rect, WIDE_STORY)
    cursor += 112 + GUTTER

    # Closing block: a rule, a heading, then the briefs joined by dots.
    painter.rectangle([EDGE, cursor, PAGE - EDGE, cursor + 3], fill=YELLOW)
    spot = paint_text(painter, EDGE, cursor + 11, "ALSO TODAY",
                      typeface(17, heavy=True), YELLOW, SPAN, 21)
    joined = "  /  ".join(BRIEF_ITEMS)
    paint_text(painter, EDGE, spot + 4, joined, typeface(16), WHITE, SPAN, 21)

    note = "Wire reports of 22 November 2026 - One page, one day"
    note_face = typeface(13)
    note_width = painter.textlength(note, font=note_face)
    painter.text(((PAGE - note_width) / 2, 990), note, font=note_face, fill=GREY)

    canvas.save(OUTPUT_FILE, format="PNG")
    return OUTPUT_FILE


if __name__ == "__main__":
    print("Rendered:", render_page())
