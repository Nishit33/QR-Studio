
# Copyright (c) 2026, Nishit Gajjar and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document
from frappe.utils import now_datetime
from frappe.utils.file_manager import save_file

from qr_studio.core.qr_generator import generate_qr_png


class QRCode(Document):

    def on_update(self):
        """Generate a QR image when the content is new or changed."""

        # Do not generate a QR code when content is empty.
        if not self.qr_content or not self.qr_content.strip():
            return

        # Avoid regenerating when only unrelated fields are changed.
        if self.qr_image and not self.has_value_changed("qr_content"):
            return

        # Generate QR image as PNG bytes.
        qr_image_data = generate_qr_png(self.qr_content)

        # Create a unique filename.
        timestamp = now_datetime().strftime("%Y%m%d%H%M%S%f")
        filename = f"{self.name}-{timestamp}.png"

        # Attach the generated image to this QR Code document.
        file_doc = save_file(
            fname=filename,
            content=qr_image_data,
            dt=self.doctype,
            dn=self.name,
            is_private=1,
        )

        # Update QR image and generation date without triggering
        # another document update.
        generated_time = now_datetime()

        self.db_set(
            {
                "qr_image": file_doc.file_url,
                "generated_on": generated_time,
            },
            update_modified=False,
        )
