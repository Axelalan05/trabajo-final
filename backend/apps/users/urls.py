from django.urls import path
from . import views
from apps.users.views import RegisterView

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
]
