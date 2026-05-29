"""
Social media image generation module.

This module generates a square social media post image from DLC learning-offer
metadata. The layout is inspired by existing DLC Instagram posts: a colorful
gradient background, strong typographic hierarchy, metadata at the top, a large
centered title, a short description, an embedded QR code, and a bottom branding
bar with DLC and funding logos.
"""

import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

from text_utils import clean_text_for_image, shorten_text


ASSET_DIR = "assets"
DLC_LOGO_PATH = os.path.join(ASSET_DIR, "logo_dlc.png")
FUNDER_LOGOS_PATH = os.path.join(ASSET_DIR, "foerderlogos_eu_sh.png")
LOCATION_ICON_PATH = os.path.join(ASSET_DIR, "icon_location.png")
CALENDAR_ICON_PATH = os.path.join(ASSET_DIR, "icon_calendar.png")
FONT_DIR = os.path.join(ASSET_DIR, "fonts")
WORK_SANS_REGULAR = os.path.join(FONT_DIR, "WorkSans-Regular.ttf")
WORK_SANS_BOLD = os.path.join(FONT_DIR, "WorkSans-Bold.ttf")
COLOR_THEMES = [
    ((33, 81, 176), (193, 108, 223)),   # blue → purple
    ((239, 74, 74), (240, 146, 86)),    # red → orange
    ((18, 28, 92), (76, 62, 200)),      # dark blue → violet
    ((16, 116, 104), (94, 201, 170)),   # teal → mint
    ((171, 52, 114), (238, 119, 149)),  # magenta → pink
    ((209, 132, 32), (245, 196, 92)),   # golden orange → light gold
]


def load_font(font_name: str, size: int):
    """
    Load a font if available. Fall back to Pillow's default font otherwise.
    """
    try:
        return ImageFont.truetype(font_name, size)
    except:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()


def draw_gradient_background(image: Image.Image, start_color: tuple, end_color: tuple) -> None:
    """
    Draw a horizontal gradient background.
    """
    width, height = image.size
    draw = ImageDraw.Draw(image)

    for x in range(width):
        ratio = x / width
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        draw.line((x, 0, x, height), fill=(r, g, b))


def draw_background_shapes(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    """
    Draw subtle geometric shapes to make the background less flat.
    """
    draw.polygon(
        [(0, 120), (width * 0.55, 0), (width, 0), (width, 350), (250, 700), (0, 560)],
        fill=(255, 255, 255, 25),
    )

    draw.polygon(
        [(width * 0.15, height), (width * 0.75, height * 0.55), (width, height * 0.75), (width, height)],
        fill=(255, 255, 255, 18),
    )

    draw.rectangle(
        (width * 0.68, 0, width * 0.78, height - 130),
        fill=(255, 255, 255, 18),
    )


def text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple:
    """
    Return text width and height using textbbox.
    """
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered_lines(
    draw: ImageDraw.ImageDraw,
    lines: list,
    center_x: int,
    start_y: int,
    font,
    fill: tuple,
    line_spacing: int,
) -> int:
    """
    Draw multiple text lines centered around center_x.
    Returns the y-position after the last line.
    """
    y = start_y

    for line in lines:
        line_width, line_height = text_size(draw, line, font)
        draw.text((center_x - line_width / 2, y), line, font=font, fill=fill)
        y += line_height + line_spacing

    return y



def paste_image_contain(base: Image.Image, image_path: str, box: tuple) -> bool:
    """
    Paste an image into a target box while preserving aspect ratio.
    Returns True if the image was pasted successfully.
    """
    if not os.path.exists(image_path):
        return False

    try:
        img = Image.open(image_path).convert("RGBA")
        box_x1, box_y1, box_x2, box_y2 = box
        box_width = box_x2 - box_x1
        box_height = box_y2 - box_y1

        img.thumbnail((box_width, box_height))

        paste_x = box_x1 + (box_width - img.width) // 2
        paste_y = box_y1 + (box_height - img.height) // 2

        base.paste(img, (paste_x, paste_y), img)
        return True

    except:
        return False


def paste_icon(base: Image.Image, image_path: str, x: int, y: int, size: int) -> bool:
    """
    Paste a small icon with fixed size.
    Returns True if the icon was pasted successfully.
    """
    if not os.path.exists(image_path):
        return False

    try:
        icon = Image.open(image_path).convert("RGBA")
        icon.thumbnail((size, size))
        base.paste(icon, (x, y), icon)
        return True
    except:
        return False

def draw_bottom_branding_bar(image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    """
    Draw the bottom white branding bar and insert available logo assets.
    """
    width, height = image.size
    bar_height = 130
    bar_top = height - bar_height

    # Draw the white background bar
    draw.rectangle((0, bar_top, width, height), fill=(255, 255, 255))

    # DLC logo area.
    pasted_dlc = paste_image_contain(image, DLC_LOGO_PATH, (45, bar_top + 20, 330, height - 20))
    if not pasted_dlc:
        fallback_font = load_font("arial.ttf", 26)
        draw.text((70, bar_top + 42), "Digital Learning\nCampus", fill=(30, 45, 70), font=fallback_font)

    # Funding / partner logos area.
    pasted_funders = paste_image_contain(image, FUNDER_LOGOS_PATH, (390, bar_top + 18, width - 40, height - 18))
    if not pasted_funders:
        fallback_font = load_font("arial.ttf", 24)
        draw.text(
            (410, bar_top + 45),
            "Kofinanziert von der Europäischen Union | Schleswig-Holstein",
            fill=(30, 45, 70),
            font=fallback_font,
        )

    # Vertical separators similar to the reference style.
    draw.line((360, bar_top + 18, 360, height - 18), fill=(190, 190, 190), width=2)
    draw.line((690, bar_top + 18, 690, height - 18), fill=(190, 190, 190), width=2)



def generate_social_image(event: dict, qr_path: str, output_path: str) -> None:
    """
    Generate a DLC-style square social media image for one learning offer.
    """
    width, height = 1080, 1080
    image = Image.new("RGB", (width, height), color=(245, 247, 250))

    # Randomly select one gradient theme for each generated post
    start_color, end_color = random.choice(COLOR_THEMES)
    draw_gradient_background(image, start_color=start_color, end_color=end_color)

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    draw_background_shapes(overlay_draw, width, height)
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Fonts. Arial is usually available on Windows; fallback is handled.
    title_font = load_font(WORK_SANS_BOLD, 56)
    #meta_font = load_font(WORK_SANS_REGULAR, 34)
    meta_bold_font = load_font(WORK_SANS_BOLD, 36)
    desc_font = load_font(WORK_SANS_REGULAR, 36)
    small_font = load_font(WORK_SANS_REGULAR, 24)

    # Clean and shorten text for image rendering.
    title = clean_text_for_image(event["title"])
    title = shorten_text(title, 95)

    description = clean_text_for_image(event["description"])
    description = shorten_text(description, 180)

    date = clean_text_for_image(event["date"])
    time = clean_text_for_image(event["time"])
    location = clean_text_for_image(event["location"])

    # Top metadata row with icons

    # Left block: location / organizer
    paste_icon(image, LOCATION_ICON_PATH, 55, 105, 120)
    draw.text((190, 130), location, font=meta_bold_font, fill=(255, 255, 255))

    # Right block: date and time
    paste_icon(image, CALENDAR_ICON_PATH, 545, 105, 120)
    draw.text((685, 128), date, font=meta_bold_font, fill=(255, 255, 255))
    draw.text((685, 172), time, font=small_font, fill=(255, 255, 255))


    # Main title.
    title_lines = textwrap.wrap(title, width=26)
    y = 335
    y = draw_centered_lines(
        draw=draw,
        lines=title_lines[:3],
        center_x=width // 2,
        start_y=y,
        font=title_font,
        fill=(255, 255, 255),
        line_spacing=18,
    )

    # Description.
    y += 45
    desc_lines = textwrap.wrap(description, width=36)
    draw_centered_lines(
        draw=draw,
        lines=desc_lines[:5],
        center_x=width // 2,
        start_y=y,
        font=desc_font,
        fill=(255, 255, 255),
        line_spacing=16,
    )

    # QR code card.
    qr_size = 150
    qr_x = width - qr_size - 40
    qr_y = height - 130 - qr_size - 65

    # CTA icon above the QR code removed based on supervisor feedback.
    # The QR code itself remains the main call-to-action element.

    draw.rounded_rectangle(
        (qr_x - 18, qr_y - 18, qr_x + qr_size + 18, qr_y + qr_size + 46),
        radius=18,
        fill=(255, 255, 255),
    )

    qr = Image.open(qr_path).convert("RGB").resize((qr_size, qr_size))
    image.paste(qr, (qr_x, qr_y))

    qr_text = "More info"
    qr_text_width, _ = text_size(draw, qr_text, small_font)
    draw.text(
        (qr_x + qr_size / 2 - qr_text_width / 2, qr_y + qr_size + 13),
        qr_text,
        fill=(30, 45, 70),
        font=small_font,
    )

    # Bottom brand bar with DLC and funding logos.
    draw_bottom_branding_bar(image, draw)

    image.save(output_path)