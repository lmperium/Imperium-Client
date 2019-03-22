import psutil


def network_connections():
    connections = list()

    for conn in psutil.net_connections():
        connections.append(dict(
            family=conn.family,
            type=conn.type,
            local_address=conn.laddr,
            remote_address=conn.raddr,
            status=conn.status,
            process_id=conn.pid
        ))

    return connections
