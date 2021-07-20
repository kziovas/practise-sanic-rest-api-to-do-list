import aioredis
from msgpack import packb, unpackb
from injector import singleton


@singleton
class CoreRedisClient:

    def __init__(self):
        self.url = ''
        self.client: aioredis.Redis = None
    
    async def start_client(self, addr : str, port : int):
        self.url = f'redis://{addr}:{port}'
        self.client = await aioredis.create_redis_pool(self.url, timeout=10, maxsize=1)
    
    async def close(self):
        if self.client:
            self.client.close()
            await self.client.wait_closed()

    async def set(self, key : str, value : str, expire : float = 60 * 10):
        await self.client.set(key, packb(value), expire=expire)
    

    async def get_all(self,pattern : str = "*") -> dict:
        cur = b'0'

        while cur:
            cur, keys = await self.client.scan(cur, match=pattern)

        result_dict={}
        for key in keys:
            result = await self.client.get(key)
            result_unpacked=unpackb(result)
            result_dict.update({key:result_unpacked})
        
        return result_dict

    async def get_by_key(self, key : str):
        result = await self.client.get(key)

        result_unpacked = unpackb(result)

        return result_unpacked
    
    async def remove_by_key(self, key : str):
        await self.client.delete(key)

    async def add_to_list(self, key : str, list_single : list):
        await self.client.lpush(key,*list_single)
    
    async def get_all_lists(self, pattern : str = "*") -> dict:
        cur = b'0'

        keys=[]
        while cur:
            cur, key = await self.client.scan(cur, match=pattern)
            keys.extend(key)

        result_dict={}
        for key in keys:
            results_binary = await self.client.lrange(key,0,-1)

            results=[]
            for result_binary in results_binary:
                results.append(result_binary.decode('ascii'))

            key_decoded = key.decode('ascii')
            result_dict.update({key_decoded:results})

        return result_dict

