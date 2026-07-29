from rest_framework import serializers
from apps.juegos.models import Juego, UserJuego


class JuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juego
        fields = ('id', 'rawg_id', 'nombre', 'genero', 'plataforma', 'imagen_url',
                  'descripcion', 'fecha_lanzamiento', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError('El nombre no puede estar vacío.')
        return value.strip()

    def validate(self, attrs):
        nombre = attrs.get('nombre', '')
        rawg_id = attrs.get('rawg_id')

        qs_nombre = Juego.objects.filter(nombre__iexact=nombre)
        if self.instance:
            qs_nombre = qs_nombre.exclude(pk=self.instance.pk)
        if qs_nombre.exists():
            raise serializers.ValidationError('Ya existe un juego con ese nombre en el catálogo.')

        if rawg_id:
            qs_rawg = Juego.objects.filter(rawg_id=rawg_id)
            if self.instance:
                qs_rawg = qs_rawg.exclude(pk=self.instance.pk)
            if qs_rawg.exists():
                raise serializers.ValidationError('Este juego de RAWG ya está en el catálogo.')

        return attrs


class UserJuegoSerializer(serializers.ModelSerializer):
    juego = JuegoSerializer(read_only=True)
    juego_id = serializers.PrimaryKeyRelatedField(
        queryset=Juego.objects.all(), source='juego', write_only=True
    )

    class Meta:
        model = UserJuego
        fields = ('id', 'juego', 'juego_id', 'estado', 'puntaje', 'resenia', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate_puntaje(self, value):
        if value is not None and (value < 1 or value > 10):
            raise serializers.ValidationError('El puntaje debe estar entre 1 y 10.')
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        juego = attrs.get('juego')
        if request and not self.instance and UserJuego.objects.filter(user=request.user, juego=juego).exists():
            raise serializers.ValidationError('Ya estás en este juego.')
        return attrs


class JugadorSerializer(serializers.ModelSerializer):
    """
    Se usa en la lista de "quién tiene este juego en su colección"
    dentro del detalle de un juego. Expone solo lo público:
    username, estado y puntaje — nada de email ni datos sensibles.
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserJuego
        fields = ('username', 'estado', 'puntaje')