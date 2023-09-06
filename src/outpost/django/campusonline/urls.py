from django.conf.urls import url

from . import views

app_name = "campusonline"

urlpatterns = [
    url(
        r"^avatar/(?P<hash>[\w\d]+)$",
        views.PrivateAvatarView.as_view(),
        name="avatar-private",
    ),
    url(
        r"^linz/xml$",
        views.XMLView.as_view(),
        name="linz-xml",
    ),
    url(
        r"^linz/schema$",
        views.SchemaView.as_view(),
        name="linz-schema",
    ),
]
