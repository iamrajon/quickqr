import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_index_view_get(client):
    url = reverse("generator:index")
    response = client.get(url)
    assert response.status_code == 200
    assert "form" in response.context
    assert b"QuickQR" in response.content


@pytest.mark.django_db
def test_index_view_get_with_content(client):
    url = reverse("generator:index")
    response = client.get(url, {"content": "https://python.org"})
    assert response.status_code == 200
    assert response.context["qr_data_uri"] is not None
    assert response.context["generated_content"] == "https://python.org"


@pytest.mark.django_db
def test_index_view_post_html(client):
    url = reverse("generator:index")
    response = client.post(
        url,
        {
            "content": "https://djangoproject.com",
            "fill_color": "#0f172a",
            "back_color": "#ffffff",
            "box_size": 10,
            "error_correction": "M",
        },
    )
    assert response.status_code == 200
    assert response.context["qr_data_uri"] is not None
    assert response.context["generated_content"] == "https://djangoproject.com"


@pytest.mark.django_db
def test_index_view_post_ajax(client):
    url = reverse("generator:index")
    response = client.post(
        url,
        data={"content": "https://fastapi.tiangolo.com"},
        headers={"x-requested-with": "XMLHttpRequest"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "qr_data_uri" in data
    assert data["content"] == "https://fastapi.tiangolo.com"


@pytest.mark.django_db
def test_index_view_post_invalid_ajax(client):
    url = reverse("generator:index")
    response = client.post(
        url,
        data={"content": ""},
        headers={"x-requested-with": "XMLHttpRequest"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "errors" in data


@pytest.mark.django_db
def test_download_view_png(client):
    url = reverse("generator:download")
    response = client.get(
        url,
        {
            "content": "https://github.com",
            "format": "png",
        },
    )
    assert response.status_code == 200
    assert response["Content-Type"] == "image/png"
    assert 'attachment; filename="qrcode.png"' in response["Content-Disposition"]
    assert response.content.startswith(b"\x89PNG\r\n\x1a\n")


@pytest.mark.django_db
def test_download_view_svg(client):
    url = reverse("generator:download")
    response = client.get(
        url,
        {
            "content": "https://github.com",
            "format": "svg",
        },
    )
    assert response.status_code == 200
    assert response["Content-Type"] == "image/svg+xml"
    assert 'attachment; filename="qrcode.svg"' in response["Content-Disposition"]
    assert b"<svg" in response.content


@pytest.mark.django_db
def test_download_view_invalid_params(client):
    url = reverse("generator:download")
    response = client.get(url, {"content": ""})
    assert response.status_code == 400
