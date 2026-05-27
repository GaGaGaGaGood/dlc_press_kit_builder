import os
import uuid

from qr_generator import generate_qr
from image_generator import generate_social_image
from text_generator import generate_press_text
from flyer_generator import generate_flyer
from metadata_exporter import save_metadata
from zip_exporter import create_zip


def run_generation(event: dict, selected_assets: dict) -> dict:
    """
    Generate selected press kit assets for one DLC learning offer.

    Parameters:
        event:
            Structured event metadata.
        selected_assets:
            Dictionary that controls which assets should be generated.
            Example:
            {
                "qr": True,
                "social": True,
                "press_text": True,
                "flyer": False,
                "zip": True
            }

    Returns:
        A dictionary containing the output folder and generated file paths.
    """

    folder_name = "outputs/" + str(uuid.uuid4())[:6]
    os.makedirs(folder_name, exist_ok=True)

    generated_files = []

    qr_path = os.path.join(folder_name, "qr_code.png")
    social_path = os.path.join(folder_name, "social_media_post.png")
    text_path = os.path.join(folder_name, "press_text.txt")
    flyer_path = os.path.join(folder_name, "flyer.png")
    metadata_path = os.path.join(folder_name, "metadata.json")

    # Metadata is always saved, because it documents the structured input.
    save_metadata(event, metadata_path)
    generated_files.append(metadata_path)

    # QR code may be needed by other assets.
    # If social image or flyer is selected, QR code must be generated internally.
    qr_required = (
        selected_assets.get("qr", False)
        or selected_assets.get("social", False)
        or selected_assets.get("flyer", False)
    )

    if qr_required:
        generate_qr(event["url"], qr_path)

        if selected_assets.get("qr", False):
            generated_files.append(qr_path)

    if selected_assets.get("social", False):
        generate_social_image(event, qr_path, social_path)
        generated_files.append(social_path)

    if selected_assets.get("press_text", False):
        generate_press_text(event, text_path)
        generated_files.append(text_path)

    if selected_assets.get("flyer", False):
        generate_flyer(event, qr_path, flyer_path)
        generated_files.append(flyer_path)

    if selected_assets.get("zip", False):
        zip_path = create_zip(folder_name)
        generated_files.append(zip_path)

    result = {
        "output_folder": folder_name,
        "generated_files": generated_files,
    }

    print("Generation complete!")
    print("Output folder:", folder_name)
    for file in generated_files:
        print("-", file)

    return result


if __name__ == "__main__":
    event = {
        "title": "Zukunftskompetenzen im digitalen Wandel",
        "date": "29 April 2026",
        "time": "13:30",
        "location": "Lübeck",
        "description": "A learning offer about future skills and digital competencies.",
        "level": "Grundlagen",
        "language": "DE",
        "url": "https://dlc.sh/",
    }

    selected_assets = {
        "qr": True,
        "social": True,
        "press_text": True,
        "flyer": True,
        "zip": True,
    }

    run_generation(event, selected_assets)