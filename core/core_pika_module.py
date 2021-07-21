import pika
from injector import singleton
from time import sleep

@singleton
class CorePikaModule:

    def __init__(self) -> None:
        self.connection : pika.BlockingConnection = None
        self.publisher_queue_name =  None
        self.consumer_queue_name =  None
        self.consumer_run : bool = False
        

    async def start_pika_module(self, host : str):
        print("Pika module called")
        print(f'Host {host}')
        while True:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
                break
            except Exception as pika_exception:
                sleep(5)
        
        self.channel = self.connection.channel()

    async def start_pika_publisher(self, publisher_queue_name : str):
        self.publisher_queue_name = publisher_queue_name
        self.publisher_queue = self.channel.queue_declare(queue=publisher_queue_name)

    async def start_pika_consumer(self, consumer_queue_name : str):
        self.consumer_queue_name = consumer_queue_name
        self.consumer_run = True
        self.consumer_queue = self.channel.queue_declare(queue=consumer_queue_name)
        

    async def stop_pika_module(self) -> None:
        self.consumer_run = False
        self.channel.close()
        self.connection.close()

    async def publish(self, message : str):
        self.channel.basic_publish(exchange = '',
                    routing_key = self.publisher_queue_name,
                    body = message)
        print("Pika message pusblished")

    async def consume(self) -> str:
        if self.consumer_run:
            method_frame, properties, body = next(self.channel.consume(self.consumer_queue_name ))

            self.channel.basic_ack(method_frame.delivery_tag)

            yield body.decode('ascii')
        else:
            yield "Cosnumer not running"
        
    async def stop_consumer(self):
        self.consumer_run = False


