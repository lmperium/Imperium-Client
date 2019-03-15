import logging
import yaml
import os

from helper import get_system_information


def main():
    # Load configuration file as a python dictionary
    abs_path = os.path.dirname(os.path.dirname(os.getcwd()))
    file_path = abs_path + '\\config.yaml'

    with open(file_path, 'r') as stream:
        config = yaml.safe_load(stream)

    logger.info('Loaded configuration file.')

    if not config['booted']:
        # Register worker with the API.
        # Retrieve system information and send it to api
        system_information = get_system_information()
        logger.info('Retrieved system information')
    else:
        logger.info('Has been booted')


if __name__ == '__main__':
    LOG_FORMAT = '%(levelname)s :: %(asctime)s :: %(funcName)s :: %(message)s'
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    logger = logging.getLogger(__name__)

    main()
