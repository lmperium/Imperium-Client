import aiohttp
import asyncio
import json
import logging

logger = logging.getLogger(__name__)


class HTTPWorker:
    """This class serves as a wrapper for API calls to the server."""
    def __init__(self):
        self.base_url = 'http://192.168.0.19:5000/api/'

    async def register_worker(self, payload):
        url = self.base_url + 'workers'

        data = json.dumps(payload)

        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data) as resp:
                logger.info(resp.status)
                response = await resp.json()
                logger.info(response)

        return response

    async def upload_results(self, command_id, payload):

        url = self.base_url + 'results'

        payload['command_id'] = command_id
        data = json.dumps(payload)

        async with aiohttp.ClientSession() as session:
            async with session.put(url=url, data=data) as resp:
                logger.info('Sending results to api.')
                logger.info(resp.status)
                response = await resp.json()
                logger.info(response)

    async def respond_heartbeat(self):
        pass
