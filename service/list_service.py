from core import CoreRedisClient, CorePikaModule
from injector import inject, singleton

@singleton
class ListService:
    @inject
    def __init__(self, redis_client : CoreRedisClient, pika_module : CorePikaModule) -> None:
        self.counter=1
        self.user_lists = { 
            "user_id_1": []
        }
        self.todo_lists={
            "to_do_list_1":[]
        }
        self.redis_client=redis_client
        self.pika_module=pika_module
        
    async def get_all_lists_by_pattern(self, pattern : str = "*") -> dict:
        cur = b'0'

        keys=[]
        while cur:
            cur, key = await self.redis_client.client.scan(cur, match=pattern)
            keys.extend(key)

        result_dict={}
        for key in keys:
            results_binary = await self.redis_client.client.lrange(key,0,-1)

            results=[]
            for result_binary in results_binary:
                results.append(result_binary.decode('ascii'))

            key_decoded = key.decode('ascii')
            result_dict.update({key_decoded:results})

        return result_dict
        
    async def add_to_list(self, key : str, list_single : list):
        await self.redis_client.client.lpush(f'todo:list:{key}',*list_single)
        await self.pika_module.publish(key)
    
    async def get_user_task_list(self, user_id : str, user_id_pattern :str, task_list_id : str, task_list_id_pattern : str) -> dict:
        user=await self.get_all_lists_by_pattern(user_id_pattern)
        
        user_task_list_ids=user[user_id_pattern]

        task_list_with_task_id={}
        if(task_list_id in user_task_list_ids):
            task_list=await self.get_all_lists_by_pattern(task_list_id_pattern)
            
            task_list_with_task_id[task_list_id]=task_list.pop(task_list_id_pattern)
            
            user_task_list_dict={user_id:task_list_with_task_id}


        else:
            user_task_list_dict={user_id:None}

        

        return user_task_list_dict
    
    async def add_user_task_list(self, user_id : str, user_id_pattern :str, task_list_id : str, task_list_id_pattern : str, task_list : list) -> dict:
        
        user = await self.get_all_lists_by_pattern(user_id_pattern)
        
        user_task_list_ids = user[user_id_pattern]

        if not (task_list_id in user_task_list_ids):
            await self.add_to_list(user_id, [task_list_id])
        

        await self.add_to_list(task_list_id, task_list)

        user_task_list_dict = await self.get_user_task_list(user_id, user_id_pattern,  task_list_id,  task_list_id_pattern) 

        return user_task_list_dict


        



        
        
    
        

