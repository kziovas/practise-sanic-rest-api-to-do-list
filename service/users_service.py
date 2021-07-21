from core import CoreRedisClient, CorePikaModule
from injector import inject, singleton

@singleton
class UsersService:
    @inject
    def __init__(self, redis_client: CoreRedisClient, pika_module : CorePikaModule) -> None:
        self.counter = 1
        self.users_list = {"user_info_1":self.counter}
        self.redis_client = redis_client
        self.pika_module = pika_module 
    
    async def get_users(self, pattern: str="*")-> dict:
        self.users_list = await self.redis_client.get_all(pattern)
        return self.users_list
    
    async def get_user_by_key(self, key : str):
        user = await self.redis_client.get_by_key(key)
        return user
    
    async def add_user(self, user:dict)-> None:
        self.counter += 1
        await self.redis_client.set(f'user_info_{self.counter}', user["name"])

    async def remove_user(self, key:str)-> None:
        await self.redis_client.remove_by_key(key)