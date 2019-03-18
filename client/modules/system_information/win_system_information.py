import platform
import psutil


# TODO Eliminate class??
class WindowsSystemInformation:
    """Retrieves Windows system information.

    Provides Windows information such as active processes, current services,
    memory stats, and network utilities like netstat.

    system_info = {
        "system":,
        "node":,
        "release":,
        "version":,
        "machine":,
        "processor":,
        "ip_address": [namedtuple(family, address, netmask, broadcast, ptp)]
    }
    """

    def get_system_information(self) -> dict:
        """Collects basic system information.

        :returns System information
        :rtype Dictionary
        """

        system_info = dict()

        # uname() returns the following attributes: system, node, release, version, machine and processor
        for key, val in platform.uname()._asdict().items():
            system_info[key] = val

        # TODO - Searching by 'Ethernet 4' might not work for all computers
        system_info['ip_address'] = psutil.net_if_addrs()['Ethernet 4']

        return system_info

