# DLC Press Kit Builder Prototype

**Prototype Version:** v1.0

## Purpose

This prototype demonstrates how structured metadata from a Digital Learning Campus (DLC) learning offer can be transformed into selected promotional assets. It was developed as a bachelor thesis prototype to show the feasibility of an automated press kit generation workflow.

The prototype is a standalone demonstrator. It does not connect directly to the DLC backend or production system.

## Implemented Features

- GUI for manual learning-offer metadata input
- Asset type selection through checkboxes
- QR code generation
- DLC-inspired social media post generation
- Flyer/poster generation
- Press text / event summary generation
- `metadata.json` export
- ZIP bundle export
- Image preview in the GUI
- Output folder access from the GUI
- Text preprocessing for long descriptions and unsupported emoji/symbols
- Gradient background variation for generated social media posts
- Use of DLC-style icons and branding elements in the social media post template

## Required Libraries

- `pillow`
- `qrcode`

Install dependencies with:

```bash
pip install -r requirements.txt
```

Alternatively, install them manually:

```bash
pip install pillow qrcode
```

## How to Run

1. Open the project in PyCharm or another Python IDE.
2. Install the required libraries.
3. Run `app.py`.
4. Enter or load learning-offer metadata.
5. Select the assets to generate.
6. Click **Generate Press Kit**.
7. Use **Open Output Folder** to access the generated files.

## Output Files

Depending on the selected asset types, the prototype can generate:

- `metadata.json`
- `qr_code.png`
- `social_media_post.png`
- `flyer.png`
- `press_text.txt`
- `press_kit.zip`

Each generation run creates a separate output folder.

## Project Structure

- `app.py`: Tkinter GUI for metadata input, asset selection, result display, image preview, and output-folder access.
- `main.py`: Central generation controller that coordinates metadata export, asset generation, and ZIP export.
- `qr_generator.py`: Generates QR code images from learning-offer URLs.
- `image_generator.py`: Generates DLC-inspired square social media posts.
- `flyer_generator.py`: Generates A4-style flyer/poster images.
- `text_generator.py`: Generates text-based event summaries.
- `metadata_exporter.py`: Saves structured input metadata as `metadata.json`.
- `zip_exporter.py`: Bundles generated files into `press_kit.zip`.
- `text_utils.py`: Provides text cleaning, invalid Unicode handling, and text shortening utilities.
- `assets/`: Contains logo and icon assets used by the visual templates.
- `screenshots/`: Contains screenshots of the GUI and generated outputs.
- `demo_output/`: Contains one representative generated press kit example.
- `docs/`: Contains supporting documentation such as evaluation material and AI-use documentation.

## Prototype Scope

This project is a feasibility prototype, not a production-ready DLC service. Its purpose is to demonstrate how structured DLC learning-offer metadata can be transformed into selected promotional assets.

The prototype currently uses manual metadata input. Direct integration with the DLC backend, CMS, or production infrastructure is outside the current implementation scope.

## Visual Assets and Branding

The DLC logo used in this prototype was obtained from the official DLC website and is included for demonstration purposes in the context of this bachelor thesis project.

The generated social media post uses a DLC-inspired visual style, including a gradient background, icon-based metadata presentation, a QR code card, and a bottom branding bar. However, the template is not an official DLC corporate identity template.

For production use, official DLC brand assets, licensing conditions, and design guidelines should be confirmed by the DLC team.

## Known Limitations

- Metadata is entered manually.
- No direct DLC backend integration is implemented.
- Image-based descriptions are not automatically processed.
- Long descriptions are shortened using a rule-based approach.
- Flyer export is PNG only, not PDF or SVG.
- Generated assets are not yet editable in template tools such as Inkscape, Canva, or Figma.
- The social media template is DLC-inspired but not an official DLC CI template.

## Future Improvements

Potential future extensions include:

- Direct metadata import from the DLC backend or CMS
- Official DLC CI / branding integration
- Editable SVG or PDF export
- Additional promotional templates for different platforms
- Dedicated metadata fields such as `teaser_text` or `promotional_description`
- OCR or structured handling for image-based descriptions
- Improved template customization for trainers or communication staff

## License

The source code of this prototype is intended to be released under the MIT License.

Logo and branding assets are used only for prototype demonstration in the context of the DLC bachelor thesis project. For production use or redistribution, official DLC brand asset permissions should be confirmed.
