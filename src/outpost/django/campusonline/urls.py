from django.urls import re_path, path

from . import views

app_name = "campusonline"

urlpatterns = [
    re_path(
        r"^avatar/(?P<hash>[\w\d]+)$",
        views.PrivateAvatarView.as_view(),
        name="avatar-private",
    ),
    path(
        "linz/xml",
        views.XMLView.as_view(),
        name="linz-xml",
    ),
    path(
        "linz/schema",
        views.SchemaView.as_view(),
        name="linz-schema",
    ),
]
