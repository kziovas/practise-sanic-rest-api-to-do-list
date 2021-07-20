from logging import RootLogger
from injector import singleton, inject
from logging import Logger
from core import CoreRedisClient
import os


@singleton
class App:
    @inject
    def __init__(self, logger : Logger, redis_client : CoreRedisClient) -> None:
        self.logger = logger
        self.redis_client = redis_client

    async def run(self, app, loop):
        self.logger.info("App has started")

    async def initialize_redis_client(self, app, loop):
        REDIS_HOST=os.environ.get("REDIS_HOST")
        REDIS_PORT = os.environ.get("REDIS_PORT")
        await self.redis_client.start_client(REDIS_HOST, REDIS_PORT)
