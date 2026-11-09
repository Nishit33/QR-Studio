import re
from io import BytesIO

import qrcode
from qrcode.constants import ERROR_CORRECT_M


def generate_qr_png(
    content: str,
    fill_color: str = "#000000",
    back_color: str = "#FFFFFF",
    box_size: int = 10,
    border: int = 4,
) -> bytes:
    """Generate a QR code and return its PNG image as bytes."""

    if content is None or not str(content).strip():
        raise ValueError("QR content cannot be empty.")

    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", fill_color):
        raise ValueError("Invalid foreground color.")

    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", back_color):
        raise ValueError("Invalid background color.")

    if not isinstance(box_size, int) or not 1 <= box_size <= 40:
        raise ValueError("Box size must be between 1 and 40.")

    if not isinstance(border, int) or not 0 <= border <= 20:
        raise ValueError("Border must be between 0 and 20.")

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )

    qr.add_data(str(content))
    qr.make(fit=True)

    image = qr.make_image(
        fill_color=fill_color,
        back_color=back_color,
    )

    image_buffer = BytesIO()
    image.save(image_buffer, format="PNG")

    return image_buffer.getvalue()
