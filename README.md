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
- Use of DLC-style icons, Work Sans typography, and branding elements in the social media post template
- Printer-friendly flyer/poster layout with DLC dark blue header, DLC logo, and funding logos
- QR code card as the main call-to-action element in generated assets

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

The generated social media post uses a DLC-inspired visual style, including a gradient background, Work Sans typography, icon-based metadata presentation, prominent location and date/time information, a QR code card, and a bottom branding bar.

The flyer/poster template uses a more printer-friendly layout with a simple white content area, a DLC dark blue header (`#29396D`), the DLC logo at the top, and funding logos at the bottom.

For production use, official DLC brand assets, licensing conditions, and design guidelines should be confirmed by the DLC team.

## Evaluation and Boundary Testing

The prototype was tested with selected real DLC learning-offer examples and additional boundary cases. The boundary tests include short titles, long titles, long compound words, long descriptions, German special characters, and missing optional metadata fields.

These tests are used to identify the current layout behavior and the limitations of the prototype. The goal is not to cover all possible DLC learning-offer cases, but to document which cases were considered and which cases would require future layout or metadata-handling improvements.

The detailed evaluation table is included in `docs/prototype_evaluation_test_cases.xlsx`.

## Known Limitations

- Metadata is entered manually.
- No direct DLC backend integration is implemented.
- Image-based descriptions are not automatically processed.
- Long descriptions are shortened using a rule-based approach.
- Flyer export is PNG only, not PDF or SVG.
- Generated assets are not yet editable in template tools such as Inkscape, Canva, or Figma.
- The social media template is DLC-inspired but not an official DLC CI template.
- Recurring events or learning offers with multiple dates are not explicitly supported.
- Very long titles, long compound words, or unusually long metadata entries may require additional layout strategies such as automatic font scaling, hyphenation, or alternative templates.
- Missing metadata fields such as date or time are not yet replaced by user-friendly placeholders.
- Multilingual layouts beyond German/English have not been systematically tested.
- Backgrounds for social media posts are generated procedurally; predefined background graphics are not yet supported.

## Future Improvements

Potential future extensions include:

- Direct metadata import from the DLC backend or CMS
- Official DLC CI / branding integration
- Additional promotional templates for different platforms
- Support for recurring events and learning offers with multiple dates
- Automatic layout adaptation for very long titles, long compound words, and missing metadata fields
- User-friendly placeholders such as “Date to be announced” for incomplete metadata
- Predefined background graphics for social media formats
- Editable SVG or PDF export for further adaptation in tools such as Inkscape, Canva, or Figma
- Additional metadata fields such as `teaser_text`, `promotional_description`, `short_title`, or `platform_specific_text`
- Extended multilingual testing and layout adaptation
- OCR or structured handling for image-based descriptions
- Improved template customization for trainers or communication staff

## License

The source code of this prototype is released under the MIT License.

Logo and branding assets are used only for prototype demonstration in the context of the DLC bachelor thesis project. For production use or redistribution, official DLC brand asset permissions should be confirmed.