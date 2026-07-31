from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('token/refresh/', views.RefreshView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('me/', views.MeView.as_view()),
    path('users/<str:username>/', views.ProfilePublicoView.as_view()),
    path('password-reset/', views.RequestPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/', views.ResetPasswordView.as_view(), name='password-reset-confirm'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('admin/users/', views.AdminUserListView.as_view(), name='admin-users'),
    path('admin/users/<int:pk>/', views.AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/users/<int:pk>/delete/', views.AdminUserDeleteView.as_view(), name='admin-user-delete'),
]