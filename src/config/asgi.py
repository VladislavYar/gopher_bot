import os
from typing import Callable

from django_asgi_lifespan.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_application = get_asgi_application()


async def application(scope: dict, receive: Callable, send: Callable) -> None:
    if scope['type'] in {'http', 'lifespan'}:
        await django_application(scope, receive, send)
    else:
        raise NotImplementedError(f'Unknown scope type {scope["type"]}')
