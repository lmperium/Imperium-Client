import aiohttp
import asyncio
import json
import logging

logger = logging.getLogger(__name__)


class HTTPWorker:
    """This class serves as a wrapper for API calls to the server."""
    def __init__(self):
        self.base_url = 'http://192.168.0.9:5000/api/'

    async def register_worker(self, payload):
        url = self.base_url + 'workers'

        data = json.dumps(payload)

        headers = {'content-type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data, headers=headers) as resp:
                logger.info(resp.status)
                response = await resp.json()
                logger.info(response)

        return response

    async def upload_results(self, command_id, payload):
        url = self.base_url + 'jobs/results'

        data = dict(command_id=command_id, response=str(payload))
        data = json.dumps(data)

        headers = {'content-type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            async with session.put(url=url, data=data, headers=headers) as resp:
                logger.info('Sending results to api.')
                logger.info(resp.status)
                response = await resp.json()
                logger.info(response)

    async def send_heartbeat(self, target_queue):
        url = self.base_url + 'heartbeats'

        data = dict(target_queue=target_queue)
        data = json.dumps(data)

        headers = {'content-type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            async with session.put(url=url, data=data, headers=headers) as resp:
                logger.info('Sending heartbeat...')
                logger.info(f'Request status: {resp.status}')
                response = await resp.json()
                logger.info(f'Response: {response}')
