from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("items/", include("items.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("seed/", include("seed.urls")),
    path("chats/", include("chats.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
