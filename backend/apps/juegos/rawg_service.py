import requests
from django.conf import settings

RAWG_BASE_URL = 'https://api.rawg.io/api'


class RawgError(Exception):
    """Error al comunicarse con la API de RAWG."""
    pass


def _armar_genero(juego: dict) -> str:
    return ', '.join(g['name'] for g in juego.get('genres', []) or [])


def _armar_plataforma(juego: dict) -> str:
    return ', '.join(p['platform']['name'] for p in juego.get('platforms', []) or [])


def buscar_juegos(query: str, page_size: int = 10) -> list[dict]:
    if not settings.RAWG_API_KEY:
        raise RawgError('RAWG_API_KEY no está configurada en el servidor.')

    try:
        response = requests.get(
            f'{RAWG_BASE_URL}/games',
            params={'key': settings.RAWG_API_KEY, 'search': query, 'page_size': page_size},
            timeout=8,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RawgError(f'No se pudo conectar con RAWG: {exc}') from exc

    data = response.json()
    return [
        {
            'rawg_id': juego.get('id'),
            'nombre': juego.get('name'),
            'imagen_url': juego.get('background_image'),
            'fecha_lanzamiento': juego.get('released'),
            'genero': _armar_genero(juego),
            'plataforma': _armar_plataforma(juego),
        }
        for juego in data.get('results', [])
    ]


def obtener_detalle(rawg_id: int) -> dict:
    if not settings.RAWG_API_KEY:
        raise RawgError('RAWG_API_KEY no está configurada en el servidor.')

    try:
        response = requests.get(
            f'{RAWG_BASE_URL}/games/{rawg_id}',
            params={'key': settings.RAWG_API_KEY},
            timeout=8,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RawgError(f'No se pudo conectar con RAWG: {exc}') from exc

    juego = response.json()
    return {
        'rawg_id': juego.get('id'),
        'nombre': juego.get('name'),
        'imagen_url': juego.get('background_image'),
        'fecha_lanzamiento': juego.get('released'),
        'genero': _armar_genero(juego),
        'plataforma': _armar_plataforma(juego),
        'descripcion': juego.get('description_raw', '') or '',
    }