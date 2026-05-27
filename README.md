Project: DLC Press Kit Builder Prototype

Prototype Version: v1.0

Purpose:
This prototype demonstrates how structured metadata from a DLC learning offer can be transformed into promotional assets.

Implemented Features:
- GUI for manual learning-offer metadata input
- Asset type selection
- QR code generation
- Social media image generation
- Flyer/poster generation
- Press text generation
- metadata.json export
- ZIP bundle export
- Image preview
- Output folder access
- Text preprocessing for long descriptions and unsupported emoji/symbols

Required Libraries:
- pillow
- qrcode

How to Run:
1. Open the project in PyCharm.
2. Install pillow and qrcode.
3. Run app.py.
4. Enter or load learning-offer metadata.
5. Select assets.
6. Click Generate Press Kit.

Output Files:
- metadata.json
- qr_code.png
- social_media_post.png
- flyer.png
- press_text.txt
- press_kit.zip

Known Limitations:
- Metadata is entered manually.
- No direct DLC backend integration is implemented.
- Image-based descriptions are not automatically processed.
- Flyer export is PNG only, not PDF or SVG.
- The social media post uses a DLC-inspired visual template, but it is not an official DLC CI template.
- Generated assets are not yet editable in template tools such as Inkscape, Canva, or Figma.

## Project Structure

- `app.py`: Tkinter GUI for metadata input, asset selection, result display, image preview, and output-folder access.
- `main.py`: Central generation controller that coordinates metadata export, asset generation, and ZIP export.
- `qr_generator.py`: Generates QR code images from learning-offer URLs.
- `image_generator.py`: Generates DLC-inspired square social media posts.
- `flyer_generator.py`: Generates A4-style flyer/poster images.
- `text_generator.py`: Generates text-based event summaries.
- `metadata_exporter.py`: Saves structured input metadata as `metadata.json`.
- `zip_exporter.py`: Bundles generated files into `press_kit.zip`.
- `text_utils.py`: Provides text cleaning, invalid Unicode handling, and shortening utilities.
- `assets/`: Contains logo and icon assets used by the image templates.

## Prototype Scope

This prototype is a standalone feasibility demonstrator. It does not connect directly to the DLC backend or production system. The purpose is to demonstrate how structured DLC learning-offer metadata can be transformed into selected promotional assets.