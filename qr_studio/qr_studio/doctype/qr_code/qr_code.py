# Copyright (c) 2026, Nishit Gajjar and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document
from frappe.utils import now_datetime
from frappe.utils.file_manager import save_file

from qr_studio.core.qr_generator import generate_qr_png


class QRCode(Document):

    def on_update(self):
        """Generate QR image when QR details are created or changed."""

        if not self.qr_content or not self.qr_content.strip():
            return

        # Regenerate only when QR-related settings change.
        qr_fields = [
            "qr_content",
            "qr_size",
            "foreground_color",
            "background_color",
            "error_correction",
        ]

        if self.qr_image and not any(
            self.has_value_changed(field) for field in qr_fields
        ):
            return

        try:
            qr_image_data = generate_qr_png(
                content=self.qr_content,
                fill_color=self.foreground_color or "#000000",
                back_color=self.background_color or "#FFFFFF",
                box_size=self.qr_size or 10,
                error_correction=self.error_correction or "M",
            )

        except ValueError as error:
            frappe.throw(str(error))

        # Create a unique filename.
        timestamp = now_datetime().strftime("%Y%m%d%H%M%S%f")
        filename = f"{self.name}-{timestamp}.png"

        # Attach the generated image to this document.
        file_doc = save_file(
            fname=filename,
            content=qr_image_data,
            dt=self.doctype,
            dn=self.name,
            is_private=1,
        )

        # Update image and generation date.
        self.db_set(
            {
                "qr_image": file_doc.file_url,
                "generated_on": now_datetime(),
            },
            update_modified=False,
        )