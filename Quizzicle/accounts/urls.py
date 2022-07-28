from django.urls import path

from django.contrib.auth import views as auth_views

from accounts import views
from accounts.forms import UserPasswordResetForm, UserSetPasswordForm

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),

    path("verify/", views.verify_user, name="verify"),
    path("resend/", views.resend_verification, name="resend_verify"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/request_reset.html", form_class=UserPasswordResetForm), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/request_confirmation.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset.html", form_class=UserSetPasswordForm), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset_complete.html"), name="password_reset_complete"),

    path("test/", views.test, name="test"),
]