from generator.forms import QRCodeForm
from generator.services import ErrorCorrectionLevel


def test_qr_form_valid():
    form = QRCodeForm(
        data={
            "content": "https://docs.djangoproject.com",
            "fill_color": "#000000",
            "back_color": "#ffffff",
            "box_size": 10,
            "error_correction": "M",
        }
    )
    assert form.is_valid()
    config = form.to_config()
    assert config.data == "https://docs.djangoproject.com"
    assert config.fill_color == "#000000"
    assert config.error_correction == ErrorCorrectionLevel.MEDIUM


def test_qr_form_empty_content():
    form = QRCodeForm(data={"content": "   "})
    assert not form.is_valid()
    assert "content" in form.errors


def test_qr_form_invalid_hex_color():
    form = QRCodeForm(
        data={
            "content": "https://example.com",
            "fill_color": "not-a-hex",
        }
    )
    assert not form.is_valid()
    assert "fill_color" in form.errors


def test_qr_form_defaults():
    form = QRCodeForm(data={"content": "Hello World"})
    assert form.is_valid()
    config = form.to_config()
    assert config.fill_color == "#0f172a"
    assert config.back_color == "#ffffff"
    assert config.box_size == 10
    assert config.error_correction == ErrorCorrectionLevel.MEDIUM
