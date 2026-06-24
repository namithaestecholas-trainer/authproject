from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_view, register_view, logout_view, dashboard_view



urlpatterns = [
    # Home Page (Redirects to Dashboard if logged in, otherwise to Login)
    path("", home_view, name="home"),

    # Authentication URLs
    path(
        "register/",
        register_view,
        name="register"
    ),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
        ),
        name="login"
    ),

   path(
       'logout/', 
       logout_view, name='logout'
       ),
    
    path(
        "dashboard/",
        dashboard_view,
        name="dashboard"
    ),

    # Password Reset URLs
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html",
            email_template_name="password_reset_email.txt",
            subject_template_name="password_reset_subject.txt"
        ),
        name="password_reset"
    ),
    
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]