import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from main import run_generation
from text_utils import remove_invalid_surrogates


last_output_folder = None
preview_image_ref = None


def generate():
    global last_output_folder

    event = {
        "title": remove_invalid_surrogates(entry_title.get().strip()),
        "date": remove_invalid_surrogates(entry_date.get().strip()),
        "time": remove_invalid_surrogates(entry_time.get().strip()),
        "location": remove_invalid_surrogates(entry_location.get().strip()),
        "description": remove_invalid_surrogates(text_description.get("1.0", tk.END).strip()),
        "level": remove_invalid_surrogates(entry_level.get().strip()),
        "language": remove_invalid_surrogates(entry_language.get().strip()),
        "url": remove_invalid_surrogates(entry_url.get().strip()),
    }

    if not event["title"] or not event["url"]:
        messagebox.showerror("Missing input", "Please enter at least a title and a URL.")
        return

    selected_assets = {
        "qr": var_qr.get(),
        "social": var_social.get(),
        "press_text": var_press_text.get(),
        "flyer": var_flyer.get(),
        "zip": var_zip.get(),
    }

    if not any(selected_assets.values()):
        messagebox.showerror("No asset selected", "Please select at least one asset type.")
        return

    try:
        result = run_generation(event, selected_assets)
        last_output_folder = result["output_folder"]

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Generation completed.\n\n")
        result_text.insert(tk.END, f"Output folder:\n{result['output_folder']}\n\n")
        result_text.insert(tk.END, "Generated files:\n")

        for file_path in result["generated_files"]:
            result_text.insert(tk.END, f"- {file_path}\n")

        preview_generated_image(result["output_folder"])

        messagebox.showinfo("Success", "Press kit generated successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def preview_generated_image(output_folder: str):
    """
    Preview generated image in the GUI.
    Priority:
    1. social_media_post.png
    2. flyer.png
    3. qr_code.png
    """
    global preview_image_ref

    social_path = os.path.join(output_folder, "social_media_post.png")
    flyer_path = os.path.join(output_folder, "flyer.png")
    qr_path = os.path.join(output_folder, "qr_code.png")

    image_path = None

    if os.path.exists(social_path):
        image_path = social_path
    elif os.path.exists(flyer_path):
        image_path = flyer_path
    elif os.path.exists(qr_path):
        image_path = qr_path

    if image_path is None:
        preview_label.config(image="", text="No image preview available.")
        preview_label.image = None
        return

    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        img.thumbnail((420, 420))

        preview_image_ref = ImageTk.PhotoImage(img)

        preview_label.config(
            image=preview_image_ref,
            text="",
            width=420,
            height=420,
            bg="#f0f0f0"
        )

        # Prevent Python from automatically releasing the image. If this is not done, Tkinter may sometimes release the image object, causing the interface to fail to display.
        preview_label.image = preview_image_ref

    except Exception as e:
        preview_label.config(
            image="",
            text=f"Preview error:\n{e}",
            width=50,
            height=10,
            bg="#f0f0f0"
        )
        preview_label.image = None


def open_output_folder():
    if not last_output_folder:
        messagebox.showwarning("No output", "No output folder has been generated yet.")
        return

    folder_path = os.path.abspath(last_output_folder)

    if os.name == "nt":
        os.startfile(folder_path)
    else:
        messagebox.showinfo("Output folder", folder_path)


def clear_form():
    entry_title.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_time.delete(0, tk.END)
    entry_location.delete(0, tk.END)
    entry_level.delete(0, tk.END)
    entry_language.delete(0, tk.END)
    entry_url.delete(0, tk.END)
    text_description.delete("1.0", tk.END)

    result_text.delete("1.0", tk.END)
    preview_label.config(image="", text="No image generated yet.")


def load_sample_event():
    clear_form()

    entry_title.insert(0, "Zukunftskompetenzen im digitalen Wandel")
    entry_date.insert(0, "29 April 2026")
    entry_time.insert(0, "13:30")
    entry_location.insert(0, "Lübeck")
    entry_level.insert(0, "Grundlagen")
    entry_language.insert(0, "DE")
    entry_url.insert(0, "https://dlc.sh/")

    text_description.insert(
        tk.END,
        "A learning offer about future skills and digital competencies.",
    )


root = tk.Tk()
root.title("DLC Press Kit Builder Prototype")
root.geometry("1150x760")
root.minsize(1050, 700)

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_frame, padx=20, pady=15)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

right_frame = tk.Frame(main_frame, padx=20, pady=15)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# ===== Left side =====

tk.Label(
    left_frame,
    text="DLC Learning Offer Metadata",
    font=("Arial", 16, "bold")
).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))


tk.Label(left_frame, text="Title").grid(row=1, column=0, sticky="w")
entry_title = tk.Entry(left_frame, width=55)
entry_title.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 6))

tk.Label(left_frame, text="Date").grid(row=3, column=0, sticky="w")
entry_date = tk.Entry(left_frame, width=55)
entry_date.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 6))

tk.Label(left_frame, text="Time").grid(row=5, column=0, sticky="w")
entry_time = tk.Entry(left_frame, width=55)
entry_time.grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 6))

tk.Label(left_frame, text="Location").grid(row=7, column=0, sticky="w")
entry_location = tk.Entry(left_frame, width=55)
entry_location.grid(row=8, column=0, columnspan=2, sticky="w", pady=(0, 6))

tk.Label(left_frame, text="Level").grid(row=9, column=0, sticky="w")
entry_level = tk.Entry(left_frame, width=55)
entry_level.grid(row=10, column=0, columnspan=2, sticky="w", pady=(0, 6))

tk.Label(left_frame, text="Language").grid(row=11, column=0, sticky="w")
entry_language = tk.Entry(left_frame, width=55)
entry_language.grid(row=12, column=0, columnspan=2, sticky="w", pady=(0, 6))

tk.Label(left_frame, text="URL").grid(row=13, column=0, sticky="w")
entry_url = tk.Entry(left_frame, width=55)
entry_url.grid(row=14, column=0, columnspan=2, sticky="w", pady=(0, 6))

tk.Label(left_frame, text="Description").grid(row=15, column=0, sticky="w")
text_description = tk.Text(left_frame, width=55, height=4)
text_description.grid(row=16, column=0, columnspan=2, sticky="w", pady=(0, 10))

tk.Label(
    left_frame,
    text="Select assets to generate",
    font=("Arial", 12, "bold")
).grid(row=17, column=0, columnspan=2, sticky="w", pady=(5, 5))

var_qr = tk.BooleanVar(value=True)
var_social = tk.BooleanVar(value=True)
var_press_text = tk.BooleanVar(value=True)
var_flyer = tk.BooleanVar(value=True)
var_zip = tk.BooleanVar(value=True)

tk.Checkbutton(left_frame, text="QR Code", variable=var_qr).grid(row=18, column=0, sticky="w")
tk.Checkbutton(left_frame, text="Social Media Post", variable=var_social).grid(row=18, column=1, sticky="w")
tk.Checkbutton(left_frame, text="Press Text", variable=var_press_text).grid(row=19, column=0, sticky="w")
tk.Checkbutton(left_frame, text="Flyer / Poster", variable=var_flyer).grid(row=19, column=1, sticky="w")
tk.Checkbutton(left_frame, text="ZIP Bundle", variable=var_zip).grid(row=20, column=0, sticky="w")

button_frame = tk.Frame(left_frame)
button_frame.grid(row=21, column=0, columnspan=2, sticky="w", pady=(15, 5))

tk.Button(
    button_frame,
    text="Load Sample",
    command=load_sample_event,
    width=14
).pack(side=tk.LEFT, padx=(0, 8))

tk.Button(
    button_frame,
    text="Generate Press Kit",
    command=generate,
    width=18
).pack(side=tk.LEFT, padx=(0, 8))

tk.Button(
    button_frame,
    text="Open Output Folder",
    command=open_output_folder,
    width=18
).pack(side=tk.LEFT, padx=(0, 8))

tk.Button(
    button_frame,
    text="Clear",
    command=clear_form,
    width=10
).pack(side=tk.LEFT)


# ===== Right side =====

tk.Label(
    right_frame,
    text="Generation Result",
    font=("Arial", 16, "bold")
).pack(anchor="w", pady=(0, 10))

result_text = tk.Text(right_frame, width=60, height=12)
result_text.pack(anchor="w", pady=(0, 20))

tk.Label(
    right_frame,
    text="Image Preview",
    font=("Arial", 16, "bold")
).pack(anchor="w", pady=(0, 10))

preview_label = tk.Label(
    right_frame,
    text="No image generated yet.",
    width=60,
    height=25,
    bg="#f0f0f0",
    relief="solid",
    borderwidth=1
)
preview_label.pack(anchor="w")

root.mainloop()