import psutil


def get_active_processes(targets=None) -> dict:
    process_info = dict()

    for proc in psutil.process_iter(attrs=['username', 'exe', 'name', 'status']):
        try:
            if targets:
                if proc.info['name'] in targets:
                    process_info[proc.pid] = proc.info
                else:
                    continue
            else:
                process_info[proc.pid] = proc.info
        except psutil.NoSuchProcess:
            pass

    return process_info
