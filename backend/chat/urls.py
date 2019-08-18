from django.conf.urls import url

from . import views

app_name = "chat"

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'api/chat_message/create/$', views.ChatMessageCreateView.as_view(), name="create_message"),
    url(r'api/chat_message/select/$', views.ChatMessageView.as_view(), name="select_message"),
    url(r'api/chat_message/update/(?P<pk>\d+)/$', views.ChatMessageUpdateDeleteView.as_view(), name="update_message"),
]
