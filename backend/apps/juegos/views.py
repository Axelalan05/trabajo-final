from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from apps.juegos.models import Juego, UserJuego
from apps.juegos.serializers import JuegoSerializer, UserJuegoSerializer, JugadorSerializer
from apps.juegos.filters import JuegoFilter
from core.response import ApiResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from apps.juegos import rawg_service


class JuegoViewSet(viewsets.ModelViewSet):
    queryset = Juego.objects.all().order_by('-created_at')
    serializer_class = JuegoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = JuegoFilter
    ordering_fields = ['created_at', 'nombre']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, status=201)
        return ApiResponse.error(
            code="validation_error", message="Invalid data",
            details=serializer.errors, status=400
        )

    def retrieve(self, request, *args, **kwargs):
        return ApiResponse.success(data=self.get_serializer(self.get_object()).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return ApiResponse.success(data=serializer.data)
        return ApiResponse.error(
            code='validation_error', message='Invalid data',
            details=serializer.errors, status=400
        )

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return ApiResponse.success(status=204)


class JuegoPublicoListView(generics.ListAPIView):
    queryset = Juego.objects.all().order_by('-created_at')
    serializer_class = JuegoSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = JuegoFilter
    ordering_fields = ['created_at', 'nombre']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return ApiResponse.success(data=serializer.data)


class UserJuegoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserJuegoSerializer
    ordering_fields = ['puntaje', 'created_at']

    def get_queryset(self):
        return UserJuego.objects.filter(user=self.request.user).select_related('juego')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return ApiResponse.success(data=serializer.data, status=201)
        return ApiResponse.error(
            code="validation_error", message="Invalid data",
            details=serializer.errors, status=400
        )

    def retrieve(self, request, *args, **kwargs):
        return ApiResponse.success(data=self.get_serializer(self.get_object()).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return ApiResponse.success(data=serializer.data)
        return ApiResponse.error(
            code='validation_error', message='Invalid data',
            details=serializer.errors, status=400
        )

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return ApiResponse.success(status=204)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        juegos_usuario = self.get_queryset()
        completados = juegos_usuario.filter(estado='completado').count()
        promedio = juegos_usuario.aggregate(Avg('puntaje'))['puntaje__avg']
        generos = juegos_usuario.values('juego__genero').annotate(total=Count('juego__genero')).order_by('-total')
        return ApiResponse.success(data={
            'juegos_completados': completados,
            'promedio_puntaje': round(promedio, 1) if promedio else 0,
            'generos_mas_jugados': list(generos),
        })

class RawgBuscarView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return ApiResponse.error(code='validation_error', message='Falta el parámetro q', status=400)
        try:
            resultados = rawg_service.buscar_juegos(query)
        except rawg_service.RawgError as exc:
            return ApiResponse.error(code='rawg_error', message=str(exc), status=502)
        return ApiResponse.success(data=resultados)


class RawgDetalleView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, rawg_id):
        try:
            detalle = rawg_service.obtener_detalle(rawg_id)
        except rawg_service.RawgError as exc:
            return ApiResponse.error(code='rawg_error', message=str(exc), status=502)
        return ApiResponse.success(data=detalle)
    
class JuegoDetalleView(APIView):
    """
    Devuelve el detalle completo de un juego:
    - Datos del juego
    - Puntaje promedio de todos los usuarios
    - Total de reseñas
    - Si el usuario está autenticado, su UserJuego (estado, puntaje, reseña)
    """
    permission_classes = [AllowAny]

    def get(self, request, juego_id):
        try:
            juego = Juego.objects.get(pk=juego_id)
        except Juego.DoesNotExist:
            return ApiResponse.error(
                code='not_found',
                message='Juego no encontrado',
                status=404
            )

        # Calcular puntaje promedio y total de reseñas
        userjuegos = UserJuego.objects.filter(juego=juego)
        stats = userjuegos.aggregate(
            puntaje_promedio=Avg('puntaje'),
            total_resenias=Count('id')
        )

        # Serializar el juego
        juego_data = JuegoSerializer(juego).data

        # Si el usuario está autenticado, buscar su UserJuego
        mi_user_juego = None
        if request.user.is_authenticated:
            try:
                mi_user_juego_obj = userjuegos.get(user=request.user)
                mi_user_juego = UserJuegoSerializer(mi_user_juego_obj).data
            except UserJuego.DoesNotExist:
                mi_user_juego = None

        return ApiResponse.success(data={
            'juego': juego_data,
            'puntaje_promedio': round(stats['puntaje_promedio'], 1) if stats['puntaje_promedio'] else None,
            'total_resenias': stats['total_resenias'],
            'mi_user_juego': mi_user_juego,
        })


class JugadorPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class QSearchFilter(SearchFilter):
    search_param = 'q'

class JuegoJugadoresView(generics.ListAPIView):
    """
    Lista paginada (10 por página) de los usuarios que tienen este
    juego en su colección, con búsqueda en vivo por username.
    Es información pública, no requiere estar logueado.
    """
    serializer_class = JugadorSerializer
    permission_classes = [AllowAny]
    pagination_class = JugadorPagination
    filter_backends = [QSearchFilter] 
    search_fields = ['user__username']
    
    def get_queryset(self):
        return UserJuego.objects.filter(
            juego_id=self.kwargs['juego_id']
        ).select_related('user').order_by('user__username')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'data': {
                'jugadores': data,
                'total': self.paginator.page.paginator.count,
                'page': self.paginator.page.number,
                'total_pages': self.paginator.page.paginator.num_pages,
            }
        })