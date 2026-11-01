# explainer/urls.py
from django.urls import path
from . import views, api

urlpatterns = [
    path("", views.index, name="index"),
    path("api/explain/", api.ExplainAPI.as_view()),
    path("api/samples/", api.SamplesAPI.as_view()),
    path("api/history/", api.HistoryAPI.as_view()),
]