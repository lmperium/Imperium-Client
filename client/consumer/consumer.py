import aio_pika
import asyncio
import logging

logger = logging.getLogger(__name__)


class Consumer:

    EXCHANGE = 'work'

    def __init__(self, amqp_url, queue_name, loop):
        self.queue_name = queue_name
        self._url = amqp_url
        self._loop = loop

    @staticmethod
    async def _on_message(message: aio_pika.IncomingMessage):
        async with message.process():
            logger.info(message.body)
            await asyncio.sleep(1)

    async def run(self):
        connection = await aio_pika.connect_robust(
            self._url,
            loop=self._loop
        )

        channel = await connection.channel()

        work_exchange = await channel.declare_exchange(
            self.EXCHANGE,
            aio_pika.ExchangeType.DIRECT
        )

        queue = await channel.declare_queue(self.queue_name)
        await queue.bind(work_exchange)

        logger.info('Listening for incoming messages...')
        await queue.consume(self._on_message)

        return connection


