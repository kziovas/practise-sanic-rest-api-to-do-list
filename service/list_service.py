from core import CoreRedisClient
from injector import inject, singleton

@singleton
class ListService:
    @inject
    def __init__(self, redis_client: CoreRedisClient) -> None:
        self.counter=1
        self.user_lists = { 
            "user_id_1": []
        }
        self.todo_lists={
            "to_do_list_1":[]
        }
        self.redis_client=redis_client

    async def get_task_lists(self, pattern: str="*")-> dict:
        self.lists= await self.redis_client.get_all_lists(pattern)
        return self.lists
    
    async def get_user_lists(self, pattern: str="*")-> dict:
        self.lists= await self.redis_client.get_all_lists(pattern)
        return self.lists
          
    async def add_task_list(self, key : str, list_single : list) -> None:
        await self.redis_client.add_to_list(f'todo:list:{key}', list_single)

    async def add_user_list(self, key : str, list_single : list) -> None:
        await self.redis_client.add_to_list(f'todo:list:{key}', list_single)
    
    async def get_user_task_list(self, user_id : str, user_id_pattern :str, task_list_id : str, task_list_id_pattern : str) -> dict:
        user=await self.get_user_lists(user_id_pattern)
        
        user_task_list_ids=user[user_id_pattern]

        task_list_with_task_id={}
        if(task_list_id in user_task_list_ids):
            task_list=await self.get_task_lists(task_list_id_pattern)
            
            task_list_with_task_id[task_list_id]=task_list.pop(task_list_id_pattern)
            
            user_task_list_dict={user_id:task_list_with_task_id}


        else:
            user_task_list_dict={user_id:None}

        

        return user_task_list_dict
    
    async def add_user_task_list(self, user_id : str, user_id_pattern :str, task_list_id : str, task_list_id_pattern : str, task_list : list) -> dict:
        
        user = await self.get_user_lists(user_id_pattern)
        
        user_task_list_ids = user[user_id_pattern]

        if not (task_list_id in user_task_list_ids):
            await self.add_user_list(user_id, [task_list_id])
        

        await self.add_task_list(task_list_id, task_list)

        user_task_list_dict = await self.get_user_task_list(user_id, user_id_pattern,  task_list_id,  task_list_id_pattern) 

        return user_task_list_dict


        



        
        
    
        

