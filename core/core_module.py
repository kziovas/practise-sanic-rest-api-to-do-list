from logging import RootLogger
import os
from injector import provider, Module, singleton, SingletonScope
import logging
from logging import Logger


class CoreModule(Module):

    @singleton
    @provider
    def create_logger(self) -> Logger:
        logging.basicConfig(level=logging.DEBUG,
                    filename='ToDoApp.log',
                    filemode='w')
        logger=logging.getLogger("ToDoApp")
        logger.setLevel(logging.DEBUG)
        return logger

