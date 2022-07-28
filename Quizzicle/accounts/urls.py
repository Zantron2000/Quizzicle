from django.urls import path

from accounts import views

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("test/", views.test, name="test"),
    path("verify/", views.verify_user, name="verify"),
    path("resend/", views.resend_verification, name="resend_verify"),
]