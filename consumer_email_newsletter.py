from typing import TYPE_CHECKING

import logging
import time
import config

from config import (
    get_connection,
    configure_logging,
    RMQ_EXCHANGE,
)

from rabbit.common import EmailUpdatesRabbit


from pika.spec import Basic, BasicProperties

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

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

    log.warning("[ ] Updating user email for newsletters %r.", body)

    start_time = time.time()

    time.sleep(1)

    end_time = time.time()
    ch.basic_ack(delivery_tag=method.delivery_tag)
    log.warning(
        "[X] Updated user email in %.2fs, message %r is OK.",
        end_time - start_time,
        body,
    )


def main():
    configure_logging()
    with EmailUpdatesRabbit() as rabbit:
        rabbit.consume_messages(
            message_callback=process_new_message,
            queue_name=config.RMQ_QUEUE_NAME_NEWSLETTER_EMAIL_UPDATES,
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
