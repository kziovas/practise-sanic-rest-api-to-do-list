from logging import RootLogger
from injector import singleton, inject
from logging import Logger
from core import CoreRedisClient, CorePikaModule
import os


@singleton
class App:
    @inject
    def __init__(self, logger : Logger, redis_client : CoreRedisClient, pika_module : CorePikaModule) -> None:
        self.logger = logger
        self.redis_client = redis_client
        self.pika_module = pika_module

    async def run(self, app, loop):
        self.logger.info("App has started")

    async def initialize(self, app, loop):
        REDIS_HOST = os.environ.get("REDIS_HOST")
        REDIS_PORT = os.environ.get("REDIS_PORT")

        await self.redis_client.start_client(REDIS_HOST, REDIS_PORT)

        RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
        RABBITMQ_PUBLISHER_QUEUE_NAME = os.environ.get("RABBITMQ_PUBLISHER_QUEUE_NAME")

        await self.pika_module.start_pika_module(RABBITMQ_HOST)
        await self.pika_module.start_pika_publisher(RABBITMQ_PUBLISHER_QUEUE_NAME)