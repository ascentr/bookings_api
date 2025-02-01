from django.contrib.auth.views import LogoutView
from django.urls import path, include, reverse_lazy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignUpView, LoginView

app_name = "accounts"

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout')
]
