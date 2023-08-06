from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication


class OnTheFlyJSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):

    def get_jwt_value(self, token):
        return bytes(token, 'utf-8')


class TokenAuthSupportQueryString(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support querystring authentication
    in the form of "http://www.example.com/?auth_token=<token_key>"
    """
    def authenticate(self, request):
        # Check if 'token_auth' is in the request query params.
        # Give precedence to 'Authorization' header.
        # print(request.query_params['auth_token'])
        if 'auth_token' in request.query_params and \
                'HTTP_AUTHORIZATION' not in request.META:
            print("auth")
            return self.authenticate_credentials(request.query_params.get('auth_token'))
        else:
            return super(TokenAuthSupportQueryString, self).authenticate(request)

class WsTokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    see:
    https://channels.readthedocs.io/en/latest/topics/authentication.html#custom-authentication
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return WsTokenAuthMiddlewareInstance(scope, self)


@database_sync_to_async
def authenticate_helper(self, encoded_auth_token):
    return self.authenticate(encoded_auth_token)

class WsTokenAuthMiddlewareInstance(OnTheFlyJSONWebTokenAuthentication):
    """
    Token authorization middleware for Django Channels 2
    """

    def get_query_params(self, scope):
        return parse_qs(scope['query_string'].decode())

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        close_old_connections()
        query_params = self.get_query_params(self.scope)
        if "auth_token" in query_params:
            try:
                auth_token = query_params['auth_token'][0]
                (user, jwt_value) = await authenticate_helper(self, auth_token)
                self.scope['user'] = user
            except Exception as e:
                self.scope['user'] = AnonymousUser()
        inner = self.inner(self.scope)
        return await inner(receive, send)

WsTokenAuthMiddlewareStack = lambda inner: WsTokenAuthMiddleware(AuthMiddlewareStack(inner))