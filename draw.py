"""Draw the 21 November 2026 one-image newspaper front page."""

from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


WIDTH = HEIGHT = 1024
MARGIN = 28
PAPER = "#FFFFFF"
INK = "#111111"
CELL_GRAY = "#E9E9E9"
RULE_GRAY = "#8A8A8A"
SUB_GRAY = "#444444"

SERIF_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size
        )


SERIF_BOLD = load_font(SERIF_PATH, 29)
SANS_SUB = load_font(SANS_PATH, 20)


STORIES = [
    {
        "headline": "Russian missiles land in Poland",
        "sub": "NATO calls it a grave violation; Warsaw sees a provocation.",
        "meme": "missile",
    },
    {
        "headline": "Mexico captures 'El Chapo Isidro'",
        "sub": "FBI most-wanted cartel boss held; 11 killed in the backlash.",
        "meme": "wanted",
    },
    {
        "headline": "Trump delays Iran strike call",
        "sub": "No decision until after New Year as Israel urges a 4-7 day campaign.",
        "meme": "clock",
    },
    {
        "headline": "BepiColombo reaches Mercury",
        "sub": "After 8 years, ESA-JAXA craft enters orbit; only the 2nd ever.",
        "meme": "mercury",
    },
    {
        "headline": "Mosquitoes cut dengue by 69%",
        "sub": "Brazil study of 5,700 children backs Wolbachia releases.",
        "meme": "mosquito",
    },
    {
        "headline": "Kate: 'Cancer does change you'",
        "sub": "Princess opens up in 'Heal'; BBC premiere 29 November.",
        "meme": "peaks",
    },
]


def text_width(draw, text, font):
    return draw.textlength(text, font=font)


def wrap_text(draw, text, font_path, size, max_width, max_lines):
    """Wrap with textwrap, shrinking the font until every line fits."""
    while size >= 8:
        font = load_font(font_path, size)
        complete_lines = wrap(
            text,
            width=len(text),
            max_lines=max_lines,
            break_long_words=False,
            break_on_hyphens=False,
        )
        if len(complete_lines) <= max_lines and all(
            text_width(draw, line, font) <= max_width for line in complete_lines
        ):
            return complete_lines, font
        for width in range(len(text), 3, -1):
            lines = wrap(
                text,
                width=width,
                max_lines=max_lines,
                placeholder="...",
                break_long_words=False,
                break_on_hyphens=False,
            )
            if len(lines) <= max_lines and all(
                text_width(draw, line, font) <= max_width for line in lines
            ):
                if "..." not in " ".join(lines):
                    return lines, font
        size -= 1
    return [text], load_font(font_path, 8)


def draw_lines(draw, lines, font, x, y, fill, line_height, anchor="lt"):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill, anchor=anchor)
        y += line_height


def draw_missile(draw, box):
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    for step in range(11):
        ratio = step / 10.0
        px = x0 + width * (0.08 + 0.76 * ratio)
        py = y0 + height * (0.90 - 0.53 * ratio - 0.16 * ratio * ratio)
        radius = 2 if step % 2 == 0 else 1
        draw.ellipse((px - radius, py - radius, px + radius, py + radius), fill=RULE_GRAY)
    center_y = y0 + 0.55 * height
    tail = x0 + 0.16 * width
    nose_base = x0 + 0.68 * width
    nose_tip = x0 + 0.82 * width
    thickness = 0.09 * height
    draw.rectangle(
        (tail, center_y - thickness, nose_base, center_y + thickness),
        fill=INK,
    )
    draw.polygon(
        [
            (nose_base, center_y - thickness),
            (nose_tip, center_y),
            (nose_base, center_y + thickness),
        ],
        fill=INK,
    )
    draw.rectangle(
        (tail - 0.015 * width, center_y - 0.015 * height, tail, center_y + 0.015 * height),
        fill=RULE_GRAY,
    )
    for side in (-1, 1):
        fin_y = center_y + side * thickness
        draw.polygon(
            [
                (tail + 0.05 * width, fin_y),
                (tail, fin_y + side * 0.20 * height),
                (tail + 0.12 * width, fin_y),
            ],
            fill=INK,
        )
    flame_x = x0 + 0.04 * width
    draw.polygon(
        [
            (tail, center_y - 0.045 * height),
            (flame_x, center_y),
            (tail, center_y + 0.045 * height),
        ],
        fill=RULE_GRAY,
    )
    draw.polygon(
        [
            (tail, center_y - 0.02 * height),
            (flame_x + 0.04 * width, center_y),
            (tail, center_y + 0.02 * height),
        ],
        fill=INK,
    )
    question = load_font(SERIF_PATH, 62)
    draw.text(
        (x0 + 0.83 * width, y0 + 0.01 * height),
        "?",
        font=question,
        fill=INK,
        anchor="lt",
    )
    pin_x = x0 + 0.14 * width
    pin_y = y0 + 0.16 * height
    draw.ellipse(
        (pin_x - 0.045 * width, pin_y - 0.06 * height, pin_x + 0.045 * width, pin_y + 0.03 * height),
        outline=INK,
        width=2,
    )
    draw.polygon(
        [
            (pin_x - 0.045 * width, pin_y),
            (pin_x + 0.045 * width, pin_y),
            (pin_x, pin_y + 0.14 * height),
        ],
        fill=INK,
    )


def draw_wanted(draw, box):
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    poster_width = 0.92 * width
    poster_height = 0.92 * height
    left = x0 + 0.04 * width
    top = y0 + 0.06 * height
    right = left + poster_width
    bottom = top + poster_height
    draw.rectangle((left, top, right, bottom), outline=INK, width=3)
    header = load_font(SERIF_PATH, 18)
    draw.text(
        ((left + right) / 2, top + 0.10 * height),
        "WANTED",
        font=header,
        fill=INK,
        anchor="mt",
    )
    half = (left + right) / 2
    head_x = left + 0.25 * poster_width
    head_y = top + 0.42 * poster_height
    head_radius = 0.085 * poster_width
    draw.ellipse(
        (head_x - head_radius, head_y - head_radius, head_x + head_radius, head_y + head_radius),
        fill=INK,
    )
    shoulder_top = head_y + 0.85 * head_radius
    shoulder_bottom = top + 0.86 * poster_height
    draw.polygon(
        [
            (left + 0.04 * poster_width, shoulder_bottom),
            (head_x - 0.11 * poster_width, shoulder_top),
            (head_x + 0.11 * poster_width, shoulder_top),
            (half - 0.03 * poster_width, shoulder_bottom),
        ],
        fill=INK,
    )
    stamp_text = "CAUGHT"
    stamp_angle = -18
    max_width = 0.90 * poster_width
    max_height = 1.10 * poster_height
    rotated = None
    stamp_font = load_font(SERIF_PATH, 8)
    for size in range(28, 7, -1):
        candidate = load_font(SERIF_PATH, size)
        bbox = draw.textbbox((0, 0), stamp_text, font=candidate)
        layer = Image.new(
            "L", (bbox[2] - bbox[0] + 6, bbox[3] - bbox[1] + 6), 0
        )
        ImageDraw.Draw(layer).text(
            (3 - bbox[0], 3 - bbox[1]), stamp_text, font=candidate, fill=255
        )
        candidate_rotated = layer.rotate(
            stamp_angle, expand=True, resample=Image.BICUBIC
        )
        if candidate_rotated.width <= max_width and candidate_rotated.height <= max_height:
            stamp_font, rotated = candidate, candidate_rotated
            break
    if rotated is None:
        bbox = draw.textbbox((0, 0), stamp_text, font=stamp_font)
        layer = Image.new(
            "L", (bbox[2] - bbox[0] + 6, bbox[3] - bbox[1] + 6), 0
        )
        ImageDraw.Draw(layer).text(
            (3 - bbox[0], 3 - bbox[1]), stamp_text, font=stamp_font, fill=255
        )
        rotated = layer.rotate(stamp_angle, expand=True, resample=Image.BICUBIC)
    safe_left = half + 0.03 * poster_width
    safe_right = right - 0.03 * poster_width
    stamp_center_x = (safe_left + safe_right) / 2
    stamp_center_y = top + 0.62 * poster_height
    stamp_x = round(stamp_center_x - rotated.width / 2)
    stamp_y = round(stamp_center_y - rotated.height / 2)
    stamp_x = max(round(safe_left), min(stamp_x, round(safe_right - rotated.width)))
    stamp_y = max(round(top + 5), min(stamp_y, round(bottom - 5 - rotated.height)))
    draw.bitmap((stamp_x, stamp_y), rotated, fill=INK)


def draw_clock(draw, box):
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    center_x = x0 + 0.50 * width
    center_y = y0 + 0.49 * height
    radius = 0.27 * min(width, height)
    draw.ellipse(
        (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
        outline=INK,
        width=4,
    )
    draw.line((center_x, center_y, center_x, center_y - 0.7 * radius), fill=INK, width=3)
    draw.line((center_x, center_y, center_x + 0.6 * radius, center_y + 0.25 * radius), fill=INK, width=3)
    draw.ellipse((center_x - 3, center_y - 3, center_x + 3, center_y + 3), fill=INK)
    bell_radius = 0.065 * min(width, height)
    for side in (-1, 1):
        bx = center_x + side * 0.72 * radius
        by = center_y - 0.82 * radius
        draw.ellipse((bx - bell_radius, by - bell_radius, bx + bell_radius, by + bell_radius), outline=INK, width=3)
        draw.line((bx, by + bell_radius, bx, by + bell_radius + 6), fill=INK, width=2)
    zzz = load_font(SERIF_PATH, 22)
    draw.text((center_x - 0.30 * width, y0), "Zzz", font=zzz, fill=INK, anchor="lt")
    january = load_font(SANS_PATH, 16)
    draw.text(
        (center_x, y1 - 6),
        "JANUARY",
        font=january,
        fill=INK,
        anchor="mb",
    )


def draw_mercury(draw, box):
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    center = (x0 + 0.60 * width, y0 + 0.49 * height)
    radius = 0.36 * min(width, height)
    draw.ellipse(
        (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
        fill=INK,
    )
    for offset_x, offset_y, size in (
        (-0.10, -0.10, 0.075),
        (0.08, -0.02, 0.055),
        (-0.03, 0.11, 0.065),
        (0.15, 0.12, 0.040),
    ):
        cx = center[0] + offset_x * width
        cy = center[1] + offset_y * height
        draw.ellipse(
            (cx - size * width, cy - size * height, cx + size * width, cy + size * height),
            fill=RULE_GRAY,
        )
    probe_x = x0 + 0.18 * width
    probe_y = y0 + 0.29 * height
    draw.rectangle(
        (probe_x - 7, probe_y - 5, probe_x + 7, probe_y + 5),
        fill=PAPER,
        outline=INK,
        width=2,
    )
    draw.line((probe_x - 10, probe_y - 8, probe_x - 10, probe_y + 8), fill=INK, width=2)
    draw.line((probe_x + 10, probe_y - 8, probe_x + 10, probe_y + 8), fill=INK, width=2)
    draw.ellipse(
        (probe_x - 15, probe_y - 15, probe_x - 7, probe_y - 7),
        outline=INK,
        width=2,
    )
    draw.line((probe_x - 11, probe_y - 8, probe_x - 9, probe_y - 6), fill=INK, width=1)
    draw.line((probe_x + 7, probe_y, probe_x + 0.29 * width, probe_y + 0.13 * height), fill=INK, width=1)
    small = load_font(SANS_PATH, 13)
    draw.text(
        (x0 + 0.05 * width, y1 - 5),
        "FINALLY!",
        font=small,
        fill=INK,
        anchor="lb",
    )


def draw_mosquito(draw, box):
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    shield_x = x0 + 0.83 * width
    shield_y = y0 + 0.50 * height
    shield_half_width = 0.085 * width
    shield_top = shield_y - 0.20 * height
    shield_bottom = shield_y + 0.22 * height
    shield_shoulder = shield_y + 0.04 * height
    shield_radius = min(shield_half_width * 0.75, (shield_shoulder - shield_top) * 0.7)
    draw.line(
        (
            shield_x - shield_half_width,
            shield_top + shield_radius,
            shield_x - shield_half_width,
            shield_shoulder,
            shield_x,
            shield_bottom,
            shield_x + shield_half_width,
            shield_shoulder,
            shield_x + shield_half_width,
            shield_top + shield_radius,
        ),
        fill=INK,
        width=2,
        joint="curve",
    )
    draw.arc(
        (
            shield_x - shield_half_width,
            shield_top,
            shield_x - shield_half_width + 2 * shield_radius,
            shield_top + 2 * shield_radius,
        ),
        90,
        270,
        fill=INK,
        width=2,
    )
    draw.arc(
        (
            shield_x + shield_half_width - 2 * shield_radius,
            shield_top,
            shield_x + shield_half_width,
            shield_top + 2 * shield_radius,
        ),
        -90,
        90,
        fill=INK,
        width=2,
    )
    draw.line(
        (
            shield_x - shield_half_width + shield_radius,
            shield_top,
            shield_x + shield_half_width - shield_radius,
            shield_top,
        ),
        fill=INK,
        width=2,
    )
    shield_text = load_font(SANS_PATH, 15)
    draw.text(
        (shield_x, shield_y - 0.02 * height),
        "69%",
        font=shield_text,
        fill=INK,
        anchor="mm",
    )

    insect_x = x0 + 0.30 * width
    insect_y = y0 + 0.45 * height
    body_length = 45
    body_radius_y = 6
    head_x = insect_x - body_length / 2
    tail_x = insect_x + body_length / 2
    draw.ellipse(
        (
            head_x,
            insect_y - body_radius_y,
            tail_x,
            insect_y + body_radius_y,
        ),
        fill=INK,
    )
    draw.ellipse(
        (head_x - 5, insect_y - 5, head_x + 5, insect_y + 5),
        fill=INK,
    )
    proboscis_y = insect_y - 1
    draw.line(
        (head_x - 3, proboscis_y, head_x - 28, proboscis_y - 4),
        fill=INK,
        width=1,
    )
    for side in (-1, 1):
        antenna_base_x = head_x + 1
        antenna_base_y = insect_y - 4
        draw.line(
            (
                antenna_base_x,
                antenna_base_y,
                antenna_base_x - 8,
                antenna_base_y - 13,
                antenna_base_x - 14 + side * 3,
                antenna_base_y - 18,
            ),
            fill=INK,
            width=1,
        )
        wing_base_x = insect_x + 5 * side
        wing_base_y = insect_y - 3
        wing_center_x = wing_base_x + 10 * side
        wing_center_y = wing_base_y - 12
        wing = Image.new("L", (42, 26), 0)
        ImageDraw.Draw(wing).ellipse((1, 1, 40, 24), outline=255, width=2)
        rotated = wing.rotate(45 * side, expand=True, resample=Image.BICUBIC)
        draw.bitmap(
            (
                round(wing_center_x - rotated.width / 2),
                round(wing_center_y - rotated.height / 2),
            ),
            rotated,
            fill=INK,
        )
    for leg_index in range(3):
        leg_x = head_x + 8 + leg_index * 14
        spread = 12 + leg_index * 4
        draw.line(
            (
                leg_x,
                insect_y + 3,
                leg_x + spread,
                insect_y + 14,
                leg_x + spread + 8,
                insect_y + 26,
            ),
            fill=INK,
            width=1,
        )
        draw.line(
            (
                leg_x,
                insect_y + 3,
                leg_x - spread,
                insect_y + 14,
                leg_x - spread - 8,
                insect_y + 26,
            ),
            fill=INK,
            width=1,
        )
    draw.polygon(
        [
            (tail_x - 7, insect_y - 1),
            (tail_x + 22, insect_y - 23),
            (tail_x + 23, insect_y + 17),
        ],
        fill=RULE_GRAY,
        outline=INK,
    )


def draw_peaks(draw, box):
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    baseline = y0 + 0.89 * height
    mountains = [
        (x0 + 0.07 * width, y0 + 0.53 * height, x0 + 0.39 * width),
        (x0 + 0.33 * width, y0 + 0.24 * height, x0 + 0.67 * width),
        (x0 + 0.61 * width, y0 + 0.59 * height, x0 + 0.93 * width),
    ]
    for left, peak, right in mountains:
        draw.polygon(
            [(left, baseline), (peak, peak), (right, baseline)],
            fill=SUB_GRAY,
            outline=INK,
        )
    heart_x = mountains[1][1]
    heart_y = y0 + 0.09 * height
    size = 0.035 * width
    draw.ellipse(
        (heart_x - size, heart_y - size, heart_x, heart_y + 0.4 * size),
        fill=INK,
    )
    draw.ellipse(
        (heart_x, heart_y - size, heart_x + size, heart_y + 0.4 * size),
        fill=INK,
    )
    draw.polygon(
        [
            (heart_x - size, heart_y + 0.1 * size),
            (heart_x + size, heart_y + 0.1 * size),
            (heart_x, heart_y + size * 1.7),
        ],
        fill=INK,
    )


MEMES = {
    "missile": draw_missile,
    "wanted": draw_wanted,
    "clock": draw_clock,
    "mercury": draw_mercury,
    "mosquito": draw_mosquito,
    "peaks": draw_peaks,
}


def draw_story(draw, story, box, headline_size, sub_size, meme_height, fill):
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    draw.rectangle(box, fill=fill)
    draw.line((x0, y0, x1, y0), fill=INK, width=3)
    pad = 14
    meme_box = (x0 + pad, y0 + 12, x1 - pad, y0 + meme_height)
    MEMES[story["meme"]](draw, meme_box)
    text_y = meme_box[3] + 6
    available = y1 - text_y - 8
    head_font = load_font(SERIF_PATH, headline_size)
    head_lines, head_font = wrap_text(
        draw, story["headline"], SERIF_PATH, headline_size, width - 2 * pad, 2
    )
    sub_font = load_font(SANS_PATH, sub_size)
    sub_lines, sub_font = wrap_text(
        draw, story["sub"], SANS_PATH, sub_size, width - 2 * pad, 2
    )
    head_step = int(head_font.size * 1.12)
    sub_step = int(sub_font.size * 1.22)
    needed = len(head_lines) * head_step + 5 + len(sub_lines) * sub_step
    while needed > available and head_font.size > 16:
        head_font = load_font(SERIF_PATH, head_font.size - 1)
        sub_font = load_font(SANS_PATH, max(12, sub_font.size - 1))
        head_lines, head_font = wrap_text(
            draw, story["headline"], SERIF_PATH, head_font.size, width - 2 * pad, 2
        )
        sub_lines, sub_font = wrap_text(
            draw, story["sub"], SANS_PATH, sub_font.size, width - 2 * pad, 2
        )
        head_step = int(head_font.size * 1.12)
        sub_step = int(sub_font.size * 1.22)
        needed = len(head_lines) * head_step + 5 + len(sub_lines) * sub_step
    draw_lines(draw, head_lines, head_font, x0 + pad, text_y, INK, head_step)
    text_y += len(head_lines) * head_step + 5
    draw_lines(draw, sub_lines, sub_font, x0 + pad, text_y, SUB_GRAY, sub_step)


def main():
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)
    left, right = MARGIN, WIDTH - MARGIN

    masthead = load_font(SERIF_PATH, 72)
    draw.text(
        (WIDTH / 2, left + 6),
        "THE WORLD TODAY",
        font=masthead,
        fill=INK,
        anchor="mt",
    )
    rule_y = left + 88
    draw.line((left, rule_y, right, rule_y), fill=RULE_GRAY, width=2)
    dateline = load_font(SANS_PATH, 18)
    draw.text((left, rule_y + 6), "SATURDAY, 21 NOVEMBER 2026", font=dateline, fill=SUB_GRAY, anchor="lt")
    draw.text((right, rule_y + 6), "ONE-IMAGE EDITION", font=dateline, fill=SUB_GRAY, anchor="rt")
    masthead_bottom = rule_y + 30
    draw.line((left, masthead_bottom, right, masthead_bottom), fill=INK, width=4)

    lead_top = masthead_bottom + 12
    lead_bottom = lead_top + 215
    lead = STORIES[0]
    lead_head = load_font(SERIF_PATH, 52)
    meme_side = 170
    text_right = right - meme_side - 170
    head_lines, lead_head = wrap_text(
        draw, lead["headline"], SERIF_PATH, 52, text_right - left - 14, 2
    )
    lead_sub = load_font(SANS_PATH, 22)
    sub_lines, lead_sub = wrap_text(
        draw, lead["sub"], SANS_PATH, 22, text_right - left - 14, 2
    )
    draw_lines(draw, head_lines, lead_head, left, lead_top + 8, INK, int(lead_head.size * 1.12))
    sub_y = lead_top + 8 + len(head_lines) * int(lead_head.size * 1.12) + 8
    draw_lines(draw, sub_lines, lead_sub, left, sub_y, SUB_GRAY, int(lead_sub.size * 1.25))
    draw_missile(
        draw,
        (right - meme_side, lead_top + 8, right, lead_top + 8 + meme_side),
    )
    draw.line((left, lead_bottom, right, lead_bottom), fill=RULE_GRAY, width=2)

    grid_top = lead_bottom + 14
    row_gap = 16
    cell_gap = 16
    first_row_height = 208
    second_row_height = HEIGHT - MARGIN - 32 - (grid_top + first_row_height + row_gap)
    available_width = right - left - 2 * cell_gap
    first_width = available_width / 3
    second_width = available_width / 2
    for index, story in enumerate(STORIES[1:]):
        if index < 3:
            cell = (
                left + index * (first_width + cell_gap),
                grid_top,
                left + index * (first_width + cell_gap) + first_width,
                grid_top + first_row_height,
            )
            meme_height = 96
        else:
            slot = index - 3
            cell = (
                left + slot * (second_width + cell_gap),
                grid_top + first_row_height + row_gap,
                left + slot * (second_width + cell_gap) + second_width,
                grid_top + first_row_height + row_gap + second_row_height,
            )
            meme_height = 128
        cell = tuple(round(value) for value in cell)
        draw_story(
            draw,
            story,
            cell,
            headline_size=29,
            sub_size=20,
            meme_height=meme_height,
            fill=PAPER if index % 2 == 0 else CELL_GRAY,
        )

    footer_font = load_font(SANS_PATH, 18)
    draw.text(
        (WIDTH / 2, HEIGHT - MARGIN + 2),
        "All six stories happened or were first reported on 21 November 2026.",
        font=footer_font,
        fill=SUB_GRAY,
        anchor="mt",
    )
    image.save("entry.png")


if __name__ == "__main__":
    main()
