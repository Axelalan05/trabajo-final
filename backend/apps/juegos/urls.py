from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.juegos import views

router = DefaultRouter()
router.register(r'mis-juegos', views.UserJuegoViewSet, basename='userjuego')
router.register(r'', views.JuegoViewSet, basename='juego')

urlpatterns = [
    path('publico/', views.JuegoPublicoListView.as_view()),
    path('rawg/buscar/', views.RawgBuscarView.as_view()),
    path('rawg/<int:rawg_id>/', views.RawgDetalleView.as_view()),
    path('<int:juego_id>/detalle/', views.JuegoDetalleView.as_view()),
    path('', include(router.urls)),
]