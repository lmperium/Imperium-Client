import glob

from bitstring import ConstBitStream


def search(file_target, search_params):
    """Searches for a file in the user's system."""
    results = dict()

    # Search by given path
    path = search_params['path'] + file_target
    path = '\\'.join(path.split('\\\\'))

    paths = glob.glob(pathname=path, recursive=True)

    results['files_found'] = paths
    results['results'] = len(paths)

    return results


def search_content(path, byte_sequence):
    results = dict()
    results['byte_sequence'] = byte_sequence
    results['files_found'] = list()
    results['errors'] = list()

    path = '\\'.join(path.split('\\\\'))
    paths = glob.glob(path, recursive=True)
    for file in paths:
        try:
            stream = ConstBitStream(filename=file)
            if stream.find(byte_sequence):
                results['files_found'].append(file)
        except PermissionError:
            results['errors'].append(f'Insufficient permissions for file: {file}')
        except ValueError:
            pass

    return results
