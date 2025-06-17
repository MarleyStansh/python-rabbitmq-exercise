from typing import TYPE_CHECKING

import logging
import time

from config import (
    get_connection,
    configure_logging,
    RMQ_EXCHANGE,
    RMQ_ROUTING_KEY,
)

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties

log = logging.getLogger(__name__)


def process_new_message(
    ch: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes,
):
    log.info("ch: %s", ch)
    log.info("method: %s", method)
    log.info("properties: %s", properties)
    log.info("body: %s", body)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    log.warning("Finished processing message %r", body)


def consume_messages(channel: "BlockingChannel"):
    channel.basic_consume(
        queue=RMQ_ROUTING_KEY,
        on_message_callback=process_new_message,
    )
    log.warning("Waiting for messages")
    channel.start_consuming()


def main():
    configure_logging()
    with get_connection() as connection:
        log.info(
            "Created connection: %s",
            connection,
        )
        with connection.channel() as channel:
            log.info("Created channel: %s", channel)
            consume_messages(channel=channel)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
