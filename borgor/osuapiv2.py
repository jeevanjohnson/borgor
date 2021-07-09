# Api v2 is still in work
# so this will be unfinished until
# api v2 is finished

import time
from enum import Enum
from enum import unique
from typing import Union
from typing import Optional
from aiohttp import ClientSession

@unique
class RankingType(Enum):
    Charts = 'charts'
    Country = 'country'
    Preformance = 'preformance'
    Score = 'score'

@unique
class BeatmapType(Enum):
    Favourite = 'favourite'
    Graveyard = 'graveyard'
    Loved = 'loved'
    Most_Played = 'most_played'
    Pending = 'pending'
    Ranked = 'ranked'

str_to_num = {
    'osu': 0,
    'taiko': 1,
    'fruits': 2,
    'mania': 3
}

@unique
class Gamemode(Enum):
    STD = 'osu'
    Taiko = 'taiko'
    Ctb = 'fruits'
    Mania = 'mania'

    def _as_int(self) -> int:
        """Use this if `Gamemode.as_int` doesn't work"""
        return str_to_num[self._value_]

    @property
    def as_int(self) -> int:
        return str_to_num[self._value_]
    
    @classmethod
    def from_int(cls, i: int) -> 'Gamemode':
        return (cls.STD, cls.Taiko, cls.Ctb, cls.Mania)[i]

class OsuApiV2:
    def __init__(
        self, client_id: int,
        client_secret: str,
        raise_errors: bool = False,
        client: Optional[ClientSession] = None
    ) -> None:

        self.client_id = client_id
        self.client_secret = client_secret
        self.token: Optional[Token] = None
        self.raise_errors = raise_errors
        self.client = client or ClientSession()
    
    async def get_json(
        self, url: str, 
        headers: dict,
        params: dict
    ) -> Optional[Union[list[dict], dict]]:

        async with self.client.get(
            url, headers = headers, 
            params = params
        ) as resp:
            if not resp:
                if self.raise_errors:
                    raise Exception('response was not found.')
                else:
                    return
            
            if resp.status != 200:
                if self.raise_errors:
                    raise Exception(f'expected 200 response code, got {resp.status}')
                else:
                    return
            
            return await resp.json()

    async def get_user_scores(
        self, userid: int, 
        type: str, params: dict = {}
    ) -> Optional[Union[list[dict], dict]]:
        if not self.token or self.token.expired:
            await self.get_access_token()
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        headers |= self.token.headers
    
        url = ('https://osu.ppy.sh/api/v2'
               f'/users/{userid}/scores/{type}')
        
        return await self.get_json(
            url, headers = headers, 
            params = params
        )
        
    async def get_me(
        self, mode: Optional[Gamemode] = None
    ) -> Optional[Union[list[dict], dict]]:
        if not self.token or self.token.expired:
            await self.get_access_token()
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        headers |= self.token.headers
    
        url = 'https://osu.ppy.sh/api/v2/me/'
        if mode: url += mode._value_
        
        return await self.get_json(
            url, headers = headers,
        )
    
    async def get_user_kudosu(
        self, userid: int, params: dict = {}
    ) -> Optional[Union[list[dict], dict]]: 
        if not self.token or self.token.expired:
            await self.get_access_token()
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        headers |= self.token.headers
    
        url = ('https://osu.ppy.sh/api/v2'
               f'/users/{userid}/kudosu')
        
        return await self.get_json(
            url, headers = headers, 
            params = params
        )
    
    async def get_user_beatmaps(
        self, userid: int, 
        type: BeatmapType, 
        params: dict = {}
    ) -> Optional[Union[list[dict], dict]]:
        if not self.token or self.token.expired:
            await self.get_access_token()
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        headers |= self.token.headers
    
        url = ('https://osu.ppy.sh/api/v2'
               f'/users/{userid}/beatmapsets/{type._value_}')
        
        return await self.get_json(
            url, headers = headers, 
            params = params
        )

    async def get_user_recent_activity(
        self, userid: int, params: dict = {}
    ) -> Optional[Union[list[dict], dict]]:
        if not self.token or self.token.expired:
            await self.get_access_token()
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        headers |= self.token.headers
    
        url = ('https://osu.ppy.sh/api/v2'
               f'/users/{userid}/recent_activity')
        
        return await self.get_json(
            url, headers = headers, 
            params = params
        )

    async def get_user(
        self, userid: int, 
        mode: Optional[Gamemode] = None,
        params: dict = {}
    ) -> Optional[Union[list[dict], dict]]:
        if not self.token or self.token.expired:
            await self.get_access_token()
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        headers |= self.token.headers
    
        url = ('https://osu.ppy.sh/api/v2'
               f'/users/{userid}/')
        if mode: url += mode._value_
        
        return await self.get_json(
            url, headers = headers, 
            params = params
        )

    async def get_users(
        self, params: dict = {}
    ) -> Optional[Union[list[dict], dict]]:
        if not self.token or self.token.expired:
            await self.get_access_token()
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        headers |= self.token.headers
    
        url = 'https://osu.ppy.sh/api/v2/users'
        
        return await self.get_json(
            url, headers = headers, 
            params = params
        )

    async def get_ranking(
        self, 
        mode: Gamemode, 
        type: RankingType,
        params: dict = {}
    ) -> Optional[Union[list[dict], dict]]:
        if not self.token or self.token.expired:
            await self.get_access_token()
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        headers |= self.token.headers
    
        url = ('https://osu.ppy.sh/api/v2'
               f'/users/{mode._value_}/'
               f'beatmapsets/{type._value_}')
        
        return await self.get_json(
            url, headers = headers, 
            params = params
        )
    
    async def get_access_token(self) -> None:
        url = 'https://osu.ppy.sh/oauth/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
            'scope': 'public'
        }

        async with self.client.post(url, data=data) as resp:
            if (
                not resp or 
                resp.status != 200 or 
                not (json := await resp.json())
            ):
                raise Exception("Couldn't Retrive token!")
        
        self.token = Token.from_api(json)

class Token:
    def __init__(self) -> None:
        self.token_type: str = None
        self.access_token: str = None
        self.expire_time: int = None
        self._expiration_date: float = None
        self.headers = {}
    
    @property
    def expired(self) -> bool:
        # Checks if token is expired
        return time.time() >= self._expiration_date

    @classmethod
    def from_api(cls, data: dict):
        creds = cls()

        creds.token_type = data['token_type']
        creds.access_token = data['access_token']
        creds.expire_time = data['expires_in']
        
        creds._expiration_date = time.time() + creds.expire_time
        creds.headers = {'Authorization': f'Bearer {creds.access_token}'}

        return creds