from sanic.response import json
from sanic import Blueprint
from service import ListService
from injector import inject, singleton
from logging import Logger
from sanic import Sanic


@singleton
class ListController:
    @inject
    def __init__(self, logger: Logger, list_service : ListService):
        self.logger = logger
        self.list_service=list_service

    async def add_user_list(self, user_id, task_list_id_dict : dict):
        if (task_list_id_dict):
            task_list_ids=task_list_id_dict["task_list_ids"]
        else:
            task_list_ids={"task_list_ids":[]}

        await self.list_service.add_user_list(user_id, task_list_ids)

    async def add_task_list(self, task_list_id, task_list_dict : dict):
        if (task_list_dict):
            task_list=task_list_dict["task_list"]
        else:
            task_list={"task_list":[]}

        await self.list_service.add_task_list(task_list_id, task_list)

    async def get_user_list(self, pattern : str = "*") -> list:
        user_lists= await self.list_service.get_user_lists(pattern)
        return user_lists

    async def get_task_list(self, pattern : str = "*") -> list:
        task_lists= await self.list_service.get_task_lists(pattern)
        return task_lists

    async def get_user_task_list(self, user_id : str, user_id_pattern : str, task_list_id : str, task_list_id_pattern : str) -> dict:
        user_task_list= await self.list_service.get_user_task_list(user_id, user_id_pattern, task_list_id, task_list_id_pattern)
        return user_task_list

    async def add_user_task_list(self, user_id : str, user_id_pattern : str, task_list_id : str, task_list_id_pattern : str,  task_list_dict : dict) -> dict:
        if (task_list_dict):
            task_list=task_list_dict["task_list"]
        else:
            task_list={"task_list":[]}

        user_task_list= await self.list_service.add_user_task_list(user_id, user_id_pattern, task_list_id, task_list_id_pattern, task_list)
        return user_task_list
    
    
 
def create_list_controller(list_controller: ListController, app: Sanic):

    lists_bp = Blueprint("lists")
    list_pattern="todo:list:"
    user_list_pattern=list_pattern+"user*"
    task_list_pattern=list_pattern+"task_list*"

    @lists_bp.route("/lists/users", methods =['GET'])
    async def get_user_list(request):
        lists= await list_controller.get_user_list(user_list_pattern)

        return json(lists)

    @lists_bp.route("/lists/task-lists", methods =['GET'])
    async def get_task_list(request):
        lists= await list_controller.get_task_list(task_list_pattern)

        return json(lists)
   
    @lists_bp.route("/lists/users/<user_id>", methods =['POST'])
    async def post_user_list(request,user_id):
        await list_controller.add_user_list(user_id,request.json)

        lists= await list_controller.get_user_list(user_list_pattern)

        return json(lists)

    @lists_bp.route("/lists/tasks/<task_list_id>", methods =['POST'])
    async def post_task_list(request,task_list_id):
        await list_controller.add_task_list(task_list_id,request.json)

        lists= await list_controller.get_task_list(task_list_pattern)

        return json(lists)

    @lists_bp.route("/lists/users/<user_id>/<task_list_id>", methods =['GET'])
    async def get_user_task_list(request,user_id, task_list_id):
        user_id_pattern=list_pattern+user_id
        task_list_id_pattern=list_pattern+task_list_id
        
        lists= await list_controller.get_user_task_list(user_id, user_id_pattern, task_list_id, task_list_id_pattern)

        return json(lists)

    @lists_bp.route("/lists/<user_id>/<task_list_id>", methods =['POST'])
    async def post_user_task_list(request,user_id,task_list_id):
        user_id_pattern=list_pattern+user_id
        task_list_id_pattern=list_pattern+task_list_id

        lists=await list_controller.add_user_task_list(user_id, user_id_pattern, task_list_id, task_list_id_pattern, request.json)

        return json(lists)

    app.blueprint(lists_bp)
