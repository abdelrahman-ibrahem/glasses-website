from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.sign_up),
    path('login-token/', views.login_token),
]
