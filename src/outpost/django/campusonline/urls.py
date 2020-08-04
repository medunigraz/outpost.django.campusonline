from django.conf.urls import url

from . import views

app_name = "campusonline"

urlpatterns = [
    url(
        r"^avatar/(?P<hash>[\w\d]+)$",
        views.PrivateAvatarView.as_view(),
        name="avatar-private",
    )
]
