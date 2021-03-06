import asyncio
import logging
import modules.system_information.win_system_information as sys_info
import os
import yaml

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from client.comms.HTTPWorker import HTTPWorker
from client.consumer.consumer import Consumer

# Load configuration file as a python dictionary
abs_path = os.path.dirname(os.getcwd())
file_path = abs_path + '\\config.yaml'


async def main(event_loop, scheduler):
    with open(file_path, 'r') as stream:
        config = yaml.safe_load(stream)

    logger.info('Configuration file loaded.')

    if not config['booted']:
        # Retrieve system information and send it to api
        win_info = sys_info.WindowsSystemInformation()

        init_info = dict()
        system_info = win_info.get_system_information()
        logger.info('Retrieved system information')

        # Prepare payload
        init_info['hostname'] = system_info['node']
        init_info['startup_info'] = system_info

        # Send init_info to api and register worker
        # Register worker with the API.
        http_worker = HTTPWorker()

        target_queue = await http_worker.register_worker(payload=init_info)
        logger.info(f'Received target queue: {target_queue["target_queue"]}')

        with open(file_path) as stream:
            config = yaml.safe_load(stream)
            config['target_queue'] = target_queue['target_queue']
            config['booted'] = True

        with open(file_path, 'w') as stream:
            yaml.dump(config, stream)
            logger.info(f'Added target queue {target_queue["target_queue"]} to config file')

        logger.info('Worker successfully registered.')

    with open(file_path) as f:
        config = yaml.safe_load(f)

    scheduler.add_job(HTTPWorker().send_heartbeat, 'interval', [config['target_queue']], minutes=10)
    scheduler.start()

    consumer = Consumer(
        amqp_url=config['amqp_url'],
        queue_name=config['target_queue'],
        loop=event_loop
    )
    return await consumer.run()

if __name__ == '__main__':
    LOG_FORMAT = '%(levelname)s :: %(asctime)s :: %(funcName)s :: %(message)s'
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    logger = logging.getLogger(__name__)

    scheduler = AsyncIOScheduler()

    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop, scheduler))

    if not connection:
        exit(1)

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
