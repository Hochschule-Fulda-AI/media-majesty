import os
import django

# calling django.setup() is required for django channels to work
# especially in this order before other imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mediamajesty.settings")
django.setup()


from channels.auth import AuthMiddlewareStack # noqa
from channels.routing import ProtocolTypeRouter, URLRouter # noqa
from channels.security.websocket import AllowedHostsOriginValidator # noqa
from django.core.asgi import get_asgi_application # noqa

from chats.routing import websocket_urlpatterns # noqa


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
