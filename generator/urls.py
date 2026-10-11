from django.urls import path

from generator import views

app_name = "generator"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("download/", views.download_qr_view, name="download"),
]
