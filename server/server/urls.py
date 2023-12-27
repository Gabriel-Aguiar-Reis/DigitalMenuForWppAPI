from django.contrib import admin
from django.urls import include, path

from menu.urls import urlpatterns as menu_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(menu_urls)),
]
