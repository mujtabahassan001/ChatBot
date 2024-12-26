import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')


import home.routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application= ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            home.routing.websocket_urlpatterns
        )
    ),
})