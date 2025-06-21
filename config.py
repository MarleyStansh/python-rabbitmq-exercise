import logging

import pika


RMQ_HOST = "0.0.0.0"
RMQ_PORT = 5672

RMQ_USER = "guest"
RMQ_PASSWORD = "guest"

RMQ_EXCHANGE = ""
RMQ_ROUTING_KEY = "hello"

RMQ_EMAIL_EXCHANGE_NAME = "email-updates"
RMQ_QUEUE_NAME_KYC_EMAIL_UPDATES = "kyc-email-updates"
RMQ_QUEUE_NAME_NEWSLETTER_EMAIL_UPDATES = "newsletter-email-updates"


connection_params = pika.ConnectionParameters(
    host=RMQ_HOST,
    port=RMQ_PORT,
    credentials=pika.PlainCredentials(
        username=RMQ_USER,
        password=RMQ_PASSWORD,
    ),
)


def get_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(
        parameters=connection_params,
    )


def configure_logging(level: int = logging.WARNING):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s",
    )
