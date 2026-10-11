import base64
import io
import re
from dataclasses import dataclass
from enum import StrEnum

import qrcode
from qrcode.image.svg import SvgPathImage


class ErrorCorrectionLevel(StrEnum):
    LOW = "L"
    MEDIUM = "M"
    QUARTILE = "Q"
    HIGH = "H"

    @property
    def qrcode_constant(self) -> int:
        mapping = {
            self.LOW: qrcode.constants.ERROR_CORRECT_L,
            self.MEDIUM: qrcode.constants.ERROR_CORRECT_M,
            self.QUARTILE: qrcode.constants.ERROR_CORRECT_Q,
            self.HIGH: qrcode.constants.ERROR_CORRECT_H,
        }
        return mapping[self]


HEX_COLOR_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def is_valid_hex_color(color: str) -> bool:
    """Validate standard 3 or 6 digit hex color strings."""
    return bool(HEX_COLOR_PATTERN.match(color.strip()))


@dataclass(frozen=True)
class QRCodeConfig:
    data: str
    fill_color: str = "#0f172a"
    back_color: str = "#ffffff"
    box_size: int = 10
    border: int = 2
    error_correction: ErrorCorrectionLevel = ErrorCorrectionLevel.MEDIUM

    def get_qr_instance(self) -> qrcode.QRCode:
        qr = qrcode.QRCode(
            version=None,
            error_correction=self.error_correction.qrcode_constant,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(self.data)
        qr.make(fit=True)
        return qr


class QRCodeService:
    """Service to generate QR codes in various formats (PNG bytes, Base64 URI, SVG)."""

    @staticmethod
    def generate_png_bytes(config: QRCodeConfig) -> bytes:
        qr = config.get_qr_instance()
        img = qr.make_image(
            fill_color=config.fill_color,
            back_color=config.back_color,
        )
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()

    @classmethod
    def generate_base64_data_uri(cls, config: QRCodeConfig) -> str:
        png_bytes = cls.generate_png_bytes(config)
        encoded = base64.b64encode(png_bytes).decode("ascii")
        return f"data:image/png;base64,{encoded}"

    @staticmethod
    def generate_svg(config: QRCodeConfig) -> str:
        qr = config.get_qr_instance()
        img = qr.make_image(
            image_factory=SvgPathImage,
            fill_color=config.fill_color,
            back_color=config.back_color,
        )
        buffer = io.BytesIO()
        img.save(buffer)
        return buffer.getvalue().decode("utf-8")
