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

log = logging.getLogger(__name__)


def declare_queue(
    channel: "BlockingChannel",
) -> None:
    queue = channel.queue_declare(queue=RMQ_ROUTING_KEY)
    log.info("Declared queue %r, %s", RMQ_ROUTING_KEY, queue)


def produce_message(
    channel: "BlockingChannel",
    idx: int,
) -> None:
    message_body = f"New message #{idx:02d}"
    log.debug("Publish message %s", message_body)
    channel.basic_publish(
        exchange=RMQ_EXCHANGE,
        routing_key=RMQ_ROUTING_KEY,
        body=message_body,
    )
    log.warning("Published message %s", message_body)


def main():
    configure_logging()
    with get_connection() as connection:
        log.info(
            "Created connection: %s",
            connection,
        )
        with connection.channel() as channel:
            log.info("Created channel: %s", channel)
            declare_queue(channel=channel)
            for idx in range(1, 11):
                produce_message(channel=channel, idx=idx)
                time.sleep(0.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
