import psutil
import asyncio


async def get_active_processes() -> dict:
    process_info = dict()
    for proc in psutil.process_iter(attrs=['username', 'exe', 'name', 'status']):
        try:
            process_info[proc.pid] = proc.info
        except psutil.NoSuchProcess:
            pass

    return process_info
