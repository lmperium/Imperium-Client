import asyncio
import concurrent.futures
import json
import logging

from client.comms.HTTPWorker import HTTPWorker
from client.modules.file import file_search
from client.modules.process import process
from client.modules.network import netstat

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

    def __init__(self, cmd_id, module, parameters, file_target=None):
        self.cmd_id = cmd_id
        self.module = module
        self.parameters = parameters
        self.file_target = file_target

    def is_command(self, module):
        return self.module == module


class CommandParser:

    command_id = None
    module = None
    file_target = None
    parameters = None

    def parse(self, message):

        task_list = list()

        commands = json.loads(message.decode('utf-8').replace('\'', '\"').replace('F', 'f'))

        for command in commands:
            self.command_id = command['command_id']
            self.module = command['module']

            if self.module == 'file':
                self.file_target = command['file_target']

            self.parameters = command['parameters']

            task_list.append(Command(self.command_id, self.module, self.parameters, self.file_target))

        return task_list


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
                    await http_worker.upload_results(command_id=cmd.cmd_id, payload=results)
            elif cmd.is_command('process'):
                logger.info(f'Process module called with the following parameters: {cmd.parameters}')
                results = process.get_active_processes()
                await http_worker.upload_results(command_id=cmd.cmd_id, payload=results)
            elif cmd.is_command('netstat'):
                logger.info(f'Netstat module called with the following parameters: {cmd.parameters}')
                results = netstat.network_connections()
                await http_worker.upload_results(command_id=cmd.cmd_id, payload=results)
            elif cmd.is_command('registry'):
                print('Registry executed')
            elif cmd.is_command('service'):
                pass



