from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signup_ajax/', views.signup_ajax, name="signup_ajax"),
    path('signin/', views.signin, name="signin"),
    path('signout/', auth_views.LogoutView.as_view(), name="signout"),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('profile/', views.ProfileView.as_view(), name='profile'),


]
