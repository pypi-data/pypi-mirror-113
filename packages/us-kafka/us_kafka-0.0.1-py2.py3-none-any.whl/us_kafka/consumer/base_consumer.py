from __future__ import annotations
import logging
from confluent_kafka import Consumer
from us_libraries.service.service_config import ServiceConfig, FORMAT_STRING

DEFAULT_TIMEOUT = 1.0


class BaseConsumer:

    def __init__(self, consumer_group_id: str, topic: str, timeout=None, message_handler=None) -> None:
        self.consumer_group_id = consumer_group_id
        self.topic = topic
        self.logger = logging.getLogger(__name__)
        self.Kafka_config = dict()
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.message_handler = message_handler
        self._configure_consumer()

    def _configure_consumer(self) -> None:
        # Create logger for consumer (logs will be emitted when poll() is called)
        logger = logging.getLogger('consumer')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
        logger.addHandler(handler)

        config = ServiceConfig()
        brokers = config.find_service('kafka-service', FORMAT_STRING)
        self.logger.info(f'kafka brokers {brokers}')

        self.kafka_config = {
            'bootstrap.servers': brokers,
            'group.id': str(self.consumer_group_id),
            'enable.auto.commit': True,
            'enable.auto.offset.store': False
        }
        self.logger.info(f'loading configuration {self.Kafka_config}')

        self.consumer = Consumer(**self.kafka_config, logger=logger)
        if len(self.topic) == 0:
            raise ValueError("Can not start the consumer without a topic to consume from.")
        self.consumer.subscribe([self.topic])

    def start(self) -> None:
        self.logger.info(f" Starting consumer with configuration {self.kafka_config} to consume from {self.topic}")

        while True:
            message = self.consumer.poll(self.timeout)

            if not message:
                continue
            if message.error():
                self.logger.info(f'Consumer error: {message.error()}')
                continue

            self.logger.info(f"Received message: {message.value().decode('utf-8')}")
            if self.message_handler:
                self.message_handler(message)

        self.consumer.close()
