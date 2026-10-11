from django import forms
from django.core.exceptions import ValidationError

from generator.services import ErrorCorrectionLevel, QRCodeConfig, is_valid_hex_color


class QRCodeForm(forms.Form):
    content = forms.CharField(
        label="Link or Text",
        max_length=2048,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "qr-input",
                "placeholder": "https://yourwebsite.com or enter any text...",
                "autocomplete": "off",
                "autofocus": "autofocus",
                "id": "id_content",
            }
        ),
    )
    fill_color = forms.CharField(
        label="QR Color",
        max_length=7,
        initial="#0f172a",
        required=False,
        widget=forms.TextInput(
            attrs={
                "type": "color",
                "class": "color-picker-input",
                "id": "id_fill_color",
            }
        ),
    )
    back_color = forms.CharField(
        label="Background Color",
        max_length=7,
        initial="#ffffff",
        required=False,
        widget=forms.TextInput(
            attrs={
                "type": "color",
                "class": "color-picker-input",
                "id": "id_back_color",
            }
        ),
    )
    box_size = forms.IntegerField(
        label="Size",
        initial=10,
        min_value=4,
        max_value=24,
        required=False,
        widget=forms.Select(
            choices=[
                (8, "Compact (200px)"),
                (10, "Standard (300px)"),
                (14, "High-Res (450px)"),
                (18, "Ultra-Res (600px)"),
            ],
            attrs={"class": "select-input", "id": "id_box_size"},
        ),
    )
    error_correction = forms.ChoiceField(
        label="Error Correction",
        initial=ErrorCorrectionLevel.MEDIUM.value,
        required=False,
        choices=[
            (ErrorCorrectionLevel.LOW.value, "Low (7% recovery)"),
            (ErrorCorrectionLevel.MEDIUM.value, "Medium (15% recovery)"),
            (ErrorCorrectionLevel.QUARTILE.value, "Quartile (25% recovery)"),
            (ErrorCorrectionLevel.HIGH.value, "High (30% recovery)"),
        ],
        widget=forms.Select(attrs={"class": "select-input", "id": "id_error_correction"}),
    )

    def clean_content(self) -> str:
        content = self.cleaned_data.get("content", "").strip()
        if not content:
            raise ValidationError("Please provide a valid link or text to generate a QR code.")
        return content

    def clean_fill_color(self) -> str:
        color = self.cleaned_data.get("fill_color") or "#0f172a"
        if not is_valid_hex_color(color):
            raise ValidationError("Invalid fill color hex code.")
        return color

    def clean_back_color(self) -> str:
        color = self.cleaned_data.get("back_color") or "#ffffff"
        if not is_valid_hex_color(color):
            raise ValidationError("Invalid background color hex code.")
        return color

    def clean_box_size(self) -> int:
        return self.cleaned_data.get("box_size") or 10

    def clean_error_correction(self) -> ErrorCorrectionLevel:
        val = self.cleaned_data.get("error_correction") or ErrorCorrectionLevel.MEDIUM.value
        try:
            return ErrorCorrectionLevel(val)
        except ValueError:
            return ErrorCorrectionLevel.MEDIUM

    def to_config(self) -> QRCodeConfig:
        return QRCodeConfig(
            data=self.cleaned_data["content"],
            fill_color=self.cleaned_data["fill_color"],
            back_color=self.cleaned_data["back_color"],
            box_size=self.cleaned_data["box_size"],
            error_correction=self.cleaned_data["error_correction"],
        )
