from sanic import Sanic
from api import create_user_controller,create_list_controller, UsersController, ListController
from core import CoreModule
from injector import Injector
from app import App
import os


def main():
    injector = Injector([CoreModule])

    app = injector.get(App)
    sanic_app = Sanic("ToDoSanicApp")
    users_controller=injector.get(UsersController)
    list_controller=injector.get(ListController)
    create_user_controller(users_controller,sanic_app)
    create_list_controller(list_controller,sanic_app)

    sanic_app.register_listener(app.run, "before_server_start")
    sanic_app.register_listener(app.initialize_redis_client, "before_server_start")

    APP_HOST=os.environ.get("APP_HOST")
    APP_PORT = os.environ.get("APP_PORT")

    sanic_app.run(host = APP_HOST, port = APP_PORT, debug = True)

if __name__ == "__main__":
    main()