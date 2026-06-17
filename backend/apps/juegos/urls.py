from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.juegos import views

router = DefaultRouter()
router.register(r'', views.JuegoViewSet, basename='juego')

urlpatterns = [
    path('publico/', views.JuegoPublicoListView.as_view()),
    path('', include(router.urls)),
]