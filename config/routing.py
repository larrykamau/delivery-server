from django.urls import path
from channels.auth import AuthMiddlewareStack  
from channels.routing import ProtocolTypeRouter, URLRouter

from kda.trips.consumers import KiuConsumer
from .consumers import NotificationConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('kiu/', KiuConsumer),
            path('kiu/notifications', NotificationConsumer ),
            path('kiu/notifications/(?p<stream>\w+)/$', NotificationConsumer )
        ])
    )
})