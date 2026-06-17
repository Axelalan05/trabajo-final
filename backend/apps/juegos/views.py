from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from apps.juegos.models import Juego
from apps.juegos.serializers import JuegoSerializer
from core.response import ApiResponse

# Create your views here.

class JuegoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = JuegoSerializer
    
    def get_queryset(self):
        return Juego.objects.filter(user=self.request.user)
    
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
            code="validation_error",
            message="Invalid data",
            details=serializer.errors,
            status= 400
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
            code='validation_error',
            message='Invalid data',
            details=serializer.errors,
            status=400
        )
    
    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return ApiResponse.success(status=204)