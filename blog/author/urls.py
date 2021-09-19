from django.urls import path
from author import views

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),
    path('followToggle/<str:author>/', views.followToggle, name='followToggle'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    
 ]