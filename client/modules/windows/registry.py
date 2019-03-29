import winreg

HKEYS = {
    "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_USERS": winreg.HKEY_USERS,
    "HKEY_PERFORMANCE_DATA": winreg.HKEY_PERFORMANCE_DATA,
    "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
    "HKEY_DYN_DATA": winreg.HKEY_DYN_DATA
}


def get_key(hkey, path, name=None):
    registry_info = dict()

    try:
        hkey_c = HKEYS[hkey.upper()]

        with winreg.OpenKey(hkey_c, path) as key:
            query_info = winreg.QueryInfoKey(key)
            registry_info['sub_keys'] = query_info[0]
            registry_info['key_values'] = query_info[1]
            registry_info['last_modified'] = query_info[2]

            if name:
                registry_info['value'] = winreg.QueryValueEx(key, name)
    except KeyError:
        registry_info['error'] = 'Invalid HKEY.'
    except FileNotFoundError:
        registry_info['error'] = 'File not found.'
    except OSError:
        registry_info['error'] = 'OS error.\nError while accessing registry.'

    return registry_info
