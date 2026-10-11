import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from generator.forms import QRCodeForm
from generator.services import QRCodeService


def _is_json_request(request: HttpRequest) -> bool:
    return (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or "application/json" in request.headers.get("accept", "")
        or request.content_type == "application/json"
    )


@require_http_methods(["GET", "POST"])
def index_view(request: HttpRequest) -> HttpResponse:
    """Main view for generating and viewing QR codes."""
    qr_data_uri: str | None = None
    generated_content: str | None = None

    if request.method == "POST":
        data = request.POST
        if request.content_type == "application/json" and request.body:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"success": False, "error": "Invalid JSON payload"}, status=400)

        form = QRCodeForm(data)
        if form.is_valid():
            config = form.to_config()
            qr_data_uri = QRCodeService.generate_base64_data_uri(config)
            generated_content = config.data

            if _is_json_request(request):
                return JsonResponse(
                    {
                        "success": True,
                        "qr_data_uri": qr_data_uri,
                        "content": generated_content,
                        "fill_color": config.fill_color,
                        "back_color": config.back_color,
                    }
                )
        else:
            if _is_json_request(request):
                return JsonResponse(
                    {
                        "success": False,
                        "errors": form.errors.get_json_data(),
                    },
                    status=400,
                )
    else:
        # Prepopulate with a friendly example if passed via query params, or empty
        initial_content = request.GET.get("content", "")
        initial = {"content": initial_content} if initial_content else None
        form = QRCodeForm(initial=initial)
        if initial_content:
            form = QRCodeForm({"content": initial_content})
            if form.is_valid():
                config = form.to_config()
                qr_data_uri = QRCodeService.generate_base64_data_uri(config)
                generated_content = config.data

    context = {
        "form": form,
        "qr_data_uri": qr_data_uri,
        "generated_content": generated_content,
    }
    return render(request, "generator/index.html", context)


@require_http_methods(["GET", "POST"])
def download_qr_view(request: HttpRequest) -> HttpResponse:
    """Download generated QR code as file attachment in PNG or SVG format."""
    params = request.POST if request.method == "POST" else request.GET
    form = QRCodeForm(params)
    if not form.is_valid():
        return HttpResponse("Invalid QR code parameters.", status=400)

    config = form.to_config()
    format_type = params.get("format", "png").lower()

    if format_type == "svg":
        svg_content = QRCodeService.generate_svg(config)
        response = HttpResponse(svg_content, content_type="image/svg+xml")
        response["Content-Disposition"] = 'attachment; filename="qrcode.svg"'
        return response

    # Default to PNG
    png_bytes = QRCodeService.generate_png_bytes(config)
    response = HttpResponse(png_bytes, content_type="image/png")
    response["Content-Disposition"] = 'attachment; filename="qrcode.png"'
    return response
