import asyncio
import concurrent.futures
import json
import logging

from client.comms.HTTPWorker import HTTPWorker
from client.modules.file import file_search
from client.modules.process import process
from client.modules.network import netstat
from client.modules.windows_services import services

"""
Command Format for File module:
    {
        "module": "file",
        "file_target": "test.txt",
        "parameters": {
            "is_hash": False,
            "paths": ,
            "content": ""
        }
    }

Command Format for Process list and netstat
    {
        "module": "process",
        "parameters": {
            "qty": 10,
            "target": [list of values to search for]
        }
    }
"""

logger = logging.getLogger(__name__)


class Command:

    command_id = None
    module = None
    parameters = None
    file_target = None

    def is_command(self, module):
        return self.module == module

    def from_dict(self, data):
        for attribute in ['command_id', 'module', 'parameters']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

        if 'file_target' in data and data['module'] == 'file':
            setattr(self, 'file_target', data['file_target'])


class CommandHandler:

    @staticmethod
    async def run_command(tasks):

        loop = asyncio.get_event_loop()

        http_worker = HTTPWorker()

        for cmd in tasks:
            if cmd.is_command('file'):
                logger.info(cmd.parameters['path'])
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    results = await loop.run_in_executor(
                        pool,
                        file_search.search,
                        cmd.file_target, cmd.parameters
                    )
                logger.info(results)
                if results:
                    await http_worker.upload_results(command_id=cmd.command_id, payload=results)
            elif cmd.is_command('process'):
                logger.info(f'Process module called with the following arguments: {cmd.parameters}')
                results = process.get_active_processes(cmd.parameters['targets'])
                logger.info(f'Process module executed with the following results: {results}')
                await http_worker.upload_results(command_id=cmd.command_id, payload=results)
            elif cmd.is_command('netstat'):
                logger.info(f'Netstat module called with the following arguments: {cmd.parameters}')
                results = netstat.network_connections(cmd.parameters['targets'])
                logger.info(f'Netstat module executed with the following results: {results}')
                await http_worker.upload_results(command_id=cmd.command_id, payload=results)
            elif cmd.is_command('service'):
                logger.info(f'Service module called with the following arguments: {cmd.parameters}')
                results = services.services(cmd.parameters)
                logger.info(f'Service module executed with the following results: {results}')
                await http_worker.upload_results(command_id=cmd.command_id, payload=results)
            elif cmd.is_command('registry'):
                pass


def parse(message):
    task_list = list()

    commands = json.loads(message.decode('utf-8').replace('\'', '\"').replace('F', 'f'))

    for command in commands:
        cmd = Command()
        cmd.from_dict(command)
        task_list.append(cmd)

    return task_list

