from __future__ import annotations

import threading
import logging
from us_libraries.service.service_config import ServiceConfig, FORMAT_STRING
from confluent_kafka import Producer

DEFAULT_TIMEOUT = 0


class BaseProducer:
    """
    Singleton class for producer
    """
    __lock = threading.Lock()
    __instance = None  # type: BaseProducer

    def __new__(cls, topic: str, timeout: int=None, *args, **kwargs) -> BaseProducer:
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = super(BaseProducer, cls).__new__(cls, *args, **kwargs)
                cls.__instance._logger = logging.getLogger(__name__)
            return cls.__instance

    def __init__(self, topic: str, timeout: int=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.topic = topic
        self.Kafka_config = None
        self.timeout = timeout or DEFAULT_TIMEOUT
        self._configure_producer()

    def _configure_producer(self):
        if not self.topic:
            raise ValueError("Missing topic to produce to.")
        config = ServiceConfig()
        brokers = config.find_service('kafka-service', FORMAT_STRING)
        self._logger.info(f'kafka brokers {brokers}')
        self.kafka_config = {'bootstrap.servers': brokers}
        self.producer = Producer(**self.kafka_config)

    def send(self, payload):

        try:
            # produce payload to kafka
            payload = bytes(str(payload), 'utf-8')
            self.producer.produce(self.topic, payload, callback=self.delivery_callback)

        except BufferError:
            self._logger.error(f'Local producer queue is full ({len(self.producer)} messages awaiting delivery): try again')
        self.producer.poll(self.timeout)

        # Wait until all messages have been delivered
        self._logger.info(f'Waiting for {len(self.producer)} deliveries')
        self.producer.flush()

    def delivery_callback(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            self._logger.error(f'Message delivery failed: {err}')
        else:
            self._logger.info(f'Message delivered to {msg.topic()} on partitions [{msg.partition()}] and offset {msg.offset()}')
