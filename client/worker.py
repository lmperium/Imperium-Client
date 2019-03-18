import asyncio
import logging
import modules.system_information.win_system_information as sys_info
import os
import yaml

from comms.HTTPWorker import HTTPWorker


async def main():
    # Load configuration file as a python dictionary
    abs_path = os.path.dirname(os.getcwd())
    file_path = abs_path + '\\config.yaml'

    with open(file_path, 'r') as stream:
        config = yaml.safe_load(stream)

    logger.info('Loaded configuration file.')

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

        with open(file_path, 'w') as stream:
            yaml.dump(config, stream)
            logger.info(f'Added target queue {target_queue["target_queue"]} to config file')

    else:
        logger.info('Has been booted')


if __name__ == '__main__':
    LOG_FORMAT = '%(levelname)s :: %(asctime)s :: %(funcName)s :: %(message)s'
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    logger = logging.getLogger(__name__)

    asyncio.run(main())
