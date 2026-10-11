from generator.services import (
    ErrorCorrectionLevel,
    QRCodeConfig,
    QRCodeService,
    is_valid_hex_color,
)


def test_is_valid_hex_color():
    assert is_valid_hex_color("#fff")
    assert is_valid_hex_color("#FFFFFF")
    assert is_valid_hex_color("#0f172a")
    assert is_valid_hex_color("#123456")
    assert not is_valid_hex_color("123456")
    assert not is_valid_hex_color("#12345")
    assert not is_valid_hex_color("#xyz123")
    assert not is_valid_hex_color("")


def test_generate_png_bytes_valid():
    config = QRCodeConfig(data="https://example.com")
    png_bytes = QRCodeService.generate_png_bytes(config)
    assert isinstance(png_bytes, bytes)
    assert len(png_bytes) > 0
    # PNG signature: \x89PNG\r\n\x1a\n
    assert png_bytes.startswith(b"\x89PNG\r\n\x1a\n")


def test_generate_base64_data_uri():
    config = QRCodeConfig(data="https://example.com")
    uri = QRCodeService.generate_base64_data_uri(config)
    assert uri.startswith("data:image/png;base64,")
    assert len(uri) > 50


def test_generate_svg():
    config = QRCodeConfig(data="https://example.com")
    svg_string = QRCodeService.generate_svg(config)
    assert isinstance(svg_string, str)
    assert "<svg" in svg_string
    assert "</svg>" in svg_string


def test_custom_config():
    config = QRCodeConfig(
        data="Custom Text Payload",
        fill_color="#6366f1",
        back_color="#ffffff",
        box_size=12,
        error_correction=ErrorCorrectionLevel.HIGH,
    )
    png_bytes = QRCodeService.generate_png_bytes(config)
    assert png_bytes.startswith(b"\x89PNG\r\n\x1a\n")
