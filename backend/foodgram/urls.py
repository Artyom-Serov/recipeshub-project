"""
URL configuration for foodgram project.
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('admin/v1/', admin.site.urls),
    path('api/v1/', include('api.urls')),
]
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
