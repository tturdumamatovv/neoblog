from django.urls import path

from .views import (
    CustomRegistrationView,
    CustomLoginView,
    ForgotPasswordView,
    ResetPasswordView,
    Users
)

urlpatterns = [
    path('register/', CustomRegistrationView.as_view(), name='custom-registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('users/', Users.as_view(), name='users')
]
