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

    log.warning("Start processing message (expensive task) %r", body)

    start_time = time.time()

    number = int(body[-2:])
    is_odd = number % 2

    time.sleep(1 + is_odd * 2)

    end_time = time.time()
    ch.basic_ack(delivery_tag=method.delivery_tag)
    log.warning(
        "Finished processing message %r in %.2fs",
        body,
        end_time - start_time,
    )


def consume_messages(channel: "BlockingChannel"):
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=RMQ_ROUTING_KEY,
        on_message_callback=process_new_message,
        # auto_ack=True,
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
