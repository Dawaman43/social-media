from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Registration
    path('login/', views.login_view, name='login'),  # Login
    path('logout/', views.logout_view, name='logout'),  # Logout
]
