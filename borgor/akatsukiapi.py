from aiohttp import ClientSession
from typing import Optional

BASE_API_V1 = 'https://akatsuki.pw/api/v1'
BASE_API_PEPPY = 'https://akatsuki.pw/api'

class AkatsukiApi:
    def __init__(
        self, raise_errors: bool = False, 
        client: Optional[ClientSession] = None
    ) -> None:

        self.raise_errors = raise_errors
        self.client = client or ClientSession()

    async def get_json(self, url: str, **kwargs) -> Optional[dict]:
        async with self.client.get(url, **kwargs) as resp:
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

    async def get_beatmaps(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_PEPPY}/get_beatmaps',
            params = params
        )
    
    async def get_user_peppy(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_PEPPY}/get_user',
            params = params
        )
    
    async def get_scores(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_PEPPY}/get_scores',
            params = params
        )
    
    async def get_user_best_peppy(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_PEPPY}/get_user_best',
            params = params
        )
    
    async def get_user_recent_peppy(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_PEPPY}/get_user_recent',
            params = params
        )
    
    async def get_ping(self) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/ping'
        )
    
    async def get_surprise_me(self) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/surprise_me'
        )

    async def get_users(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users',
            params = params
        )
    
    async def get_users_full(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/full',
            params = params
        )

    async def get_users_whatid(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/whatid',
            params = params
        )
    
    async def get_users_userpage(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/userpage',
            params = params
        )

    async def get_users_lookup(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/lookup',
            params = params
        )
    
    async def get_users_achievements(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/achievements',
            params = params
        )
    
    async def get_users_most_played(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/most_played',
            params = params
        )
    
    async def get_badges(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/badges',
            params = params
        )
    
    async def get_badges_members(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/badges',
            params = params
        )
    
    async def get_scores(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/scores',
            params = params
        )
    
    async def get_user_recent(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/scores/recent',
            params = params
        )
    
    async def get_user_best(
        self, params: dict
    ) -> Optional[dict]:
        return await self.get_json(
            url = f'{BASE_API_V1}/users/scores/best',
            params = params
        )