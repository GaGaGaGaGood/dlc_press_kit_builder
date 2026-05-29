import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from text_utils import clean_text_for_image, shorten_text

ASSET_DIR = "assets"
DLC_LOGO_PATH = os.path.join(ASSET_DIR, "logo_dlc.png")
FUNDER_LOGOS_PATH = os.path.join(ASSET_DIR, "foerderlogos_eu_sh.png")

FONT_DIR = os.path.join(ASSET_DIR, "fonts")
WORK_SANS_REGULAR = os.path.join(FONT_DIR, "WorkSans-Regular.ttf")
WORK_SANS_BOLD = os.path.join(FONT_DIR, "WorkSans-Bold.ttf")

DLC_DARK_BLUE = (41, 57, 109)  # #29396D
LIGHT_BACKGROUND = (248, 249, 252)
TEXT_DARK = (25, 30, 45)
TEXT_GREY = (80, 80, 80)

def load_font(font_path: str, size: int):
    """
    Load a font from a file path. Fall back to Arial or Pillow default.
    """
    try:
        return ImageFont.truetype(font_path, size)
    except:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()

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

def generate_flyer(event: dict, qr_path: str, output_path: str) -> None:
    """
    Generate an A4-style flyer/poster as a PNG image.
    """
    width, height = 1240, 1754  # Approx. A4 ratio at medium resolution

    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    title_font = load_font(WORK_SANS_BOLD, 70)
    heading_font = load_font(WORK_SANS_BOLD, 42)
    body_font = load_font(WORK_SANS_REGULAR, 34)
    body_bold_font = load_font(WORK_SANS_BOLD, 34)
    small_font = load_font(WORK_SANS_REGULAR, 26)

    description = clean_text_for_image(event["description"])
    description = shorten_text(description, 450)  # Limit text length

    # Header
    draw.rectangle((0, 0, width, 220), fill=DLC_DARK_BLUE)

    pasted_logo = paste_image_contain(image, DLC_LOGO_PATH, (60, 35, 430, 185))
    if not pasted_logo:
        draw.text((80, 75), "Digital Learning Campus", fill="white", font=heading_font)

    draw.text(
        (760, 82),
        "Learning Offer",
        fill="white",
        font=heading_font,
    )

    # Title
    y = 300
    wrapped_title = textwrap.wrap(event["title"], width=26)
    for line in wrapped_title:
        draw.text((80, y), line, fill=(20, 20, 20), font=title_font)
        y += 82

    # Event information box
    y += 40
    box_top = y
    box_bottom = y + 300
    draw.rounded_rectangle(
        (80, box_top, width - 80, box_bottom),
        radius=25,
        outline=(210, 210, 210),
        width=3,
        fill=(245, 247, 250),
    )

    info_y = y + 45
    draw.text((120, info_y), f"Date: {event['date']}", fill=(40, 40, 40), font=body_font)
    info_y += 60
    draw.text((120, info_y), f"Time: {event['time']}", fill=(40, 40, 40), font=body_font)
    info_y += 60
    draw.text((120, info_y), f"Location: {event['location']}", fill=(40, 40, 40), font=body_font)
    info_y += 60
    draw.text(
        (120, info_y),
        f"Level: {event['level']} | Language: {event['language']}",
        fill=(40, 40, 40),
        font=body_font,
    )

    # Description
    y = box_bottom + 80
    draw.text((80, y), "About this learning offer", fill=(20, 20, 20), font=heading_font)
    y += 70

    wrapped_desc = textwrap.wrap(description, width=55)
    for line in wrapped_desc[:7]:  #If the text is too long, you can adjust the line limit.
        draw.text((80, y), line, fill=(70, 70, 70), font=body_font)
        y += 48

    # QR code section
    qr = Image.open(qr_path).convert("RGB").resize((260, 260))
    image.paste(qr, (80, height - 430))

    draw.text(
        (380, height - 370),
        "Scan the QR code",
        fill=TEXT_DARK,
        font=heading_font,
    )
    draw.text(
        (380, height - 310),
        "Open the DLC learning offer page",
        fill=TEXT_GREY,
        font=body_font,
    )

    # Footer
    footer_top = height - 190
    draw.rectangle((0, footer_top, width, height), fill=(255, 255, 255))
    draw.line((80, footer_top, width - 80, footer_top), fill=(220, 220, 220), width=2)

    pasted_funders = paste_image_contain(
        image,
        FUNDER_LOGOS_PATH,
        (40, footer_top + 15, width - 40, height - 15),
    )

    if not pasted_funders:
        draw.text(
            (80, footer_top + 55),
            "Funding logos / partner logos",
            fill=TEXT_GREY,
            font=small_font,
        )

    image.save(output_path)