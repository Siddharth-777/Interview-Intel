import aio_pika

from app.core.config import settings

INGEST_QUEUE = "ingest_jobs"


async def get_rabbitmq_connection() -> aio_pika.abc.AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.RABBITMQ_URL)


async def publish_ingest_job(experience_id: str) -> None:
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(INGEST_QUEUE, durable=True)  # noqa: F841
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=experience_id.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=INGEST_QUEUE,
        )
