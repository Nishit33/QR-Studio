import re
from io import BytesIO

import qrcode
from qrcode.constants import (
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    ERROR_CORRECT_H,
)


ERROR_CORRECTION_LEVELS = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}


def generate_qr_png(
    content: str,
    fill_color: str = "#000000",
    back_color: str = "#FFFFFF",
    box_size: int = 10,
    border: int = 4,
    error_correction: str = "M",
) -> bytes:

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

    error_correction = str(error_correction).upper()

    if error_correction not in ERROR_CORRECTION_LEVELS:
        raise ValueError("Invalid error correction level.")

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECTION_LEVELS[error_correction],
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
