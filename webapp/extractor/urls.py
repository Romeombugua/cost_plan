from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("run/", views.run, name="run"),
    path("status/<str:job_id>/", views.status, name="status"),
    path("download/<str:job_id>/", views.download, name="download"),
    path("history/", views.history, name="history"),
]
