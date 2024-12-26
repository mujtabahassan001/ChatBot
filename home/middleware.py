from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
import json

class TokenAuthMiddleware(BaseMiddleware):

    async def authenticate(self, user):
        return user

    async def connect(self, scope, receive, send):
        user = self.scope.get('user', AnonymousUser())
        self.scope['user'] = user

        return await super().connect(scope, receive, send)

