from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

urlpatterns = [
    url(r'', include('chat.urls')),
    url(r'admin/$', admin.site.urls),
]
