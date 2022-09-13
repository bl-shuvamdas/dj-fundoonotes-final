from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    path('register/', views.RegisterApiView.as_view(), name="register"),
    path('login/', views.LoginApiView.as_view(), name="login"),
    path('verify/<str:token>/', views.VerifyUser.as_view(), name="verify"),
    path('signup/', views.SignUpFormView.as_view(), name="signup"),
    path('signin/', views.SignInFormView.as_view(), name="signin"),
]
