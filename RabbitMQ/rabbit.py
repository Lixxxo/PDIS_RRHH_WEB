import pika
from Models.models import Project
from utils.db import db


class Rabbit:
    """RabbitMQ class with"""

    connection = None
    channel = None

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

    def publish(self, message: str, exchange: str):
        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        self.channel.basic_publish(exchange=exchange, routing_key='', body=message)
        print(" [> publish] %r to %s exchange" % (message, exchange))

    def consume(self, exchange: str):
        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')

        result = self.channel.queue_declare(queue='', exclusive=True, durable=True, auto_delete=True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange=exchange, queue=queue_name)
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.receive_project, auto_ack=True)

        print(" [*] Started %s exchange" % exchange)
        self.channel.start_consuming()

    @staticmethod
    def receive_project(ch, method, properties, serialized_project: str):
        print(" [< received] %r" % serialized_project)
        new_project = Project.from_string(serialized_project=serialized_project)
        print("deserialized project:", new_project.to_json())

        _project = Project.query.filter_by(name=new_project.name).first()

        if _project:
            print("Project already existed")
            return

        db.session.add(new_project)
        print("Project created")
        db.session.commit()
