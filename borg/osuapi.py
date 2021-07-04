from aiohttp import ClientSession
from typing import Optional

BASE_API = 'https://osu.ppy.sh/api'

class OsuApi:
    def __init__(
        self, key: str, 
        raise_errors: bool = False, 
        client: Optional[ClientSession] = None
    ) -> None:
        self.key = key
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
        """https://github.com/ppy/osu-api/wiki#parameters"""
        if 'k' not in params:
            params['k'] = self.key
        
        return await self.get_json(
            url = f'{BASE_API}/get_beatmaps',
            params = params
        )
    
    async def get_user(
        self, params: dict
    ) -> Optional[dict]:
        """https://github.com/ppy/osu-api/wiki#parameters-1"""
        if 'k' not in params:
            params['k'] = self.key
        
        return await self.get_json(
            url = f'{BASE_API}/get_user',
            params = params
        )
    
    async def get_scores(
        self, params: dict
    ) -> Optional[dict]:
        """https://github.com/ppy/osu-api/wiki#parameters-2"""
        if 'k' not in params:
            params['k'] = self.key
        
        return await self.get_json(
            url = f'{BASE_API}/get_scores',
            params = params
        )
    
    async def get_user_best(
        self, params: dict
    ) -> Optional[dict]:
        """https://github.com/ppy/osu-api/wiki#parameters-3"""
        if 'k' not in params:
            params['k'] = self.key
        
        return await self.get_json(
            url = f'{BASE_API}/get_user_best',
            params = params
        )
    
    async def get_user_recent(
        self, params: dict
    ) -> Optional[dict]:
        """https://github.com/ppy/osu-api/wiki#parameters-4"""
        if 'k' not in params:
            params['k'] = self.key
        
        return await self.get_json(
            url = f'{BASE_API}/get_user_recent',
            params = params
        )
    
    async def get_match(
        self, params: dict
    ) -> Optional[dict]:
        """https://github.com/ppy/osu-api/wiki#parameters-5"""
        if 'k' not in params:
            params['k'] = self.key
        
        return await self.get_json(
            url = f'{BASE_API}/get_match',
            params = params
        )
    
    async def get_replay(
        self, params: dict
    ) -> Optional[dict]:
        """https://github.com/ppy/osu-api/wiki#parameters-6"""
        if 'k' not in params:
            params['k'] = self.key
        
        return await self.get_json(
            url = f'{BASE_API}/get_replay',
            params = params
        )