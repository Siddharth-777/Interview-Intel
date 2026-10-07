import json
import logging

import aio_pika

from app.core.config import settings

logger = logging.getLogger(__name__)

_connection: aio_pika.abc.AbstractRobustConnection | None = None


async def get_connection() -> aio_pika.abc.AbstractRobustConnection:
    global _connection  # noqa: PLW0603
    if _connection is None or _connection.is_closed:
        _connection = await aio_pika.connect_robust(
            settings.RABBITMQ_URL
        )
    return _connection


async def close_connection() -> None:
    global _connection  # noqa: PLW0603
    if _connection is not None and not _connection.is_closed:
        await _connection.close()
    _connection = None


async def _declare_infrastructure(
    channel: aio_pika.abc.AbstractChannel,
) -> None:
    dlx = await channel.declare_exchange(
        settings.INGEST_DLX,
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )
    dlq = await channel.declare_queue(
        settings.INGEST_DLQ, durable=True
    )
    await dlq.bind(dlx, routing_key=settings.INGEST_QUEUE)

    await channel.declare_queue(
        settings.INGEST_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": settings.INGEST_DLX,
        },
    )


async def publish_ingest_message(experience_id: str) -> None:
    connection = await get_connection()
    channel = await connection.channel()
    try:
        await _declare_infrastructure(channel)
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(
                    {"experience_id": experience_id}
                ).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json",
            ),
            routing_key=settings.INGEST_QUEUE,
        )
    finally:
        await channel.close()
