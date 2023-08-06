import functools
import os

from quart import abort, redirect, request, session

from .base import *
from .http import AioClient


class DiscordOauth2Client(AioClient):
    def __init__(self, app):
        super().__init__(app)

    async def callback(self):
        # access_token = await super().callback()
        # super(DiscordOauth2Client, self).token_updater(access_token.get('access_token'))
        discord = await self._make_session()
        access_token = await discord.fetch_token(self.token_url, client_secret=self.client_secret, authorization_response=request.url)
        super().token_updater(token=access_token)
        await discord.aclose()

    @staticmethod
    def is_logged_in(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            if session.get("DISCORD_OAUTH2_TOKEN") is not None:
                return await func(*args, **kwargs)
            else:
                abort(401)

        return wrapped

    def is_logged(self):
        if session.get("DISCORD_OAUTH2_TOKEN") is not None:
            return True
        else:
            return False

    @staticmethod
    async def logout():
        try:
            session.pop('DISCORD_OAUTH2_TOKEN')
        except:
            pass
        try:
            session.pop('DISCORD_OAUTH2_STATE')
        except:
            pass

    async def create_session(self):
        if 'http://' in self.redirect_url:
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
        discord = await self._make_session()
        authorization_url, state = discord.create_authorization_url(DISCORD_AUTHORIZATION_BASE_URL)
        session['DISCORD_OAUTH2_STATE'] = state
        # print(redirect(self.MyClient._make_session().authorization_url(DISCORD_AUTHORIZATION_BASE_URL)))
        await discord.aclose()
        return redirect(authorization_url)
