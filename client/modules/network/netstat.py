import psutil
import logging

logger = logging.getLogger(__name__)


def network_connections(targets=None) -> list:
    connections = list()
    logger.info(f'Targets {targets}')
    for conn in psutil.net_connections():
        if targets:
            if hasattr(conn.raddr, 'ip'):
                if conn.raddr.ip in targets:
                    connections.append(dict(
                        family=conn.family,
                        type=conn.type,
                        local_address=conn.laddr,
                        remote_address=conn.raddr,
                        status=conn.status,
                        process_id=conn.pid
                    ))
            else:
                continue
        else:
            connections.append(dict(
                family=conn.family,
                type=conn.type,
                local_address=conn.laddr,
                remote_address=conn.raddr,
                status=conn.status,
                process_id=conn.pid
            ))

    return connections
