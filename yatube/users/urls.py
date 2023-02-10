from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy

from users.views import SignUp, UserProfileView, IntroView
# from yatube.settings import EMAIL_HOST_USER

app_name = 'users'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        "profile/<int:pk>/", UserProfileView.as_view(), name="profile"
    ),
    path(
        'password_change/',
        PasswordChangeView.
        as_view(success_url=reverse_lazy('users:password_change_done'),
                template_name='users/password_change_form.html'),
        name='password_change'
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.
        as_view(template_name='users/password_change_done.html'),
        name='password_change_done'
    ),
    path(
        'password_reset/',
        PasswordResetView.
        as_view(success_url=reverse_lazy('users:password_reset_done'),
                template_name='users/password_reset_form.html',
                # from_email=EMAIL_HOST_USER,
                email_template_name='users/password_reset_email.html'),
        name='password_reset_form'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.
        as_view(success_url=reverse_lazy('users:password_reset_complete'),
                template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.
        as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.
        as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    path('intro', IntroView.as_view(), name='intro')
]
