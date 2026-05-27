import qrcode


def generate_qr(url: str, output_path: str) -> None:
    """
    Generate a QR code image from a URL.
    """
    qr_img = qrcode.make(url)
    qr_img.save(output_path)