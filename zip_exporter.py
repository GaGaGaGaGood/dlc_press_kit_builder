import os
import zipfile


def create_zip(output_folder: str, zip_name: str = "press_kit.zip") -> str:
    """
    Create a ZIP archive containing all generated press kit files.
    """
    zip_path = os.path.join(output_folder, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)

            if os.path.isfile(file_path) and filename != zip_name:
                zip_file.write(file_path, arcname=filename)

    return zip_path