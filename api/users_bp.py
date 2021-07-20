from sanic.response import json
from sanic import Blueprint
from service import UsersService
from injector import inject, singleton, Injector
from logging import Logger
from sanic import Sanic


@singleton
class UsersController:
    @inject
    def __init__(self, logger: Logger, users_service: UsersService):
        self.logger = logger
        self.users_service = users_service
    
    async def get_users_service(self, pattern : str ="*"):
        users = await self.users_service.get_users(pattern)
        return  users
    
    async def get_user_by_key(self, key : str):
        user = await self.users_service.get_user_by_key(key)
        return user

    async def add_user(self, user: dict):
        await self.users_service.add_user(user)
    
    async def remove_user(self, key: int):
        await self.users_service.remove_user(key)

def create_user_controller(user_controller: UsersController, app: Sanic):
    users_bp = Blueprint("users")
    users_info_pattern="todo:user_info_*"

    @users_bp.route("/users", methods =['GET'])
    async def get_users(request):
        users= await user_controller.get_users_service(users_info_pattern)
        return json(users)

    @users_bp.route("/users/<id>", methods =['GET'])
    async def get_user_by_key(request, id):
        users= await user_controller.get_user_by_key(id)
        return json(users)

    @users_bp.route("/users", methods =['POST'])
    async def post_users(request):
        await user_controller.add_user(request.json)
        users= await user_controller.get_users_service(users_info_pattern)
        return json(users)

    @users_bp.route("/users/<id>", methods =['DELETE'])
    async def delete_users(request, id):
        await user_controller.remove_user(id)
        users= await user_controller.get_users_service(users_info_pattern)
        return json(users)

    app.blueprint(users_bp)


