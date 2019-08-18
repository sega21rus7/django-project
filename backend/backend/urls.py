from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'', include('chat.urls')),
    url(r'', include('user_profile.urls')),
    url(r'admin/', admin.site.urls),
]
