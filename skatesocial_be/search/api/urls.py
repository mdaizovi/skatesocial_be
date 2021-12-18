from django.urls import include, path, re_path
from .views import SearchView

urlpatterns = [
    re_path("", SearchView.as_view(), name="search"),
]
