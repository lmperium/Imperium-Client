import asyncio
import logging
import os
import yaml

from modules.system_information import win_system_information as sys_info


async def main():
    # Load configuration file as a python dictionary
    abs_path = os.path.dirname(os.path.dirname(os.getcwd()))
    file_path = abs_path + '\\config.yaml'

    with open(file_path, 'r') as stream:
        config = yaml.safe_load(stream)

    logger.info('Loaded configuration file.')

    if not config['booted']:
        # Retrieve system information and send it to api
        win_info = sys_info.WindowsSystemInformation()

        init_info = dict()
        system_info = win_info.get_system_information()

        # Prepare payload
        init_info['hostname'] = system_info['node']
        init_info['startup_info'] = system_info

        # Send init_info to api and register worker

        logger.info(init_info)

        logger.info('Retrieved system information')
        # Register worker with the API.
    else:
        logger.info('Has been booted')


if __name__ == '__main__':
    LOG_FORMAT = '%(levelname)s :: %(asctime)s :: %(funcName)s :: %(message)s'
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    logger = logging.getLogger(__name__)

    asyncio.run(main(), debug=True)
