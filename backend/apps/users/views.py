from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print(request.data)
        return Response({'message': 'ok'})
