import asyncio
import glob


def search(file_target, search_params):
    """Searches for a file in the user's system."""
    results = dict()

    # Search by given path
    path = search_params['path'] + file_target
    path = '\\'.join(path.split('\\\\'))

    paths = glob.glob(pathname=path, recursive=True)

    if search_params['content']:
        pass

    results['files_found'] = paths
    results['results'] = len(paths)

    return results
