from django.conf.urls import url

from . import views

app_name = "user_profile"

urlpatterns = [
    url(r'^sign_out/', views.UserSignOutView.as_view(), name="sign_out"),
    url(r'api/user/select/$', views.UserView.as_view(), name="select_user"),
    url(r'api/user/create/$', views.UserCreateView.as_view(), name="create_user"),
    url(r'api/user/login/$', views.UserLoginView.as_view(), name="login_user"),
    url(r'api/user/update/(?P<pk>\d+)/$', views.UserUpdateDeleteView.as_view(), name="update_user"),
]
