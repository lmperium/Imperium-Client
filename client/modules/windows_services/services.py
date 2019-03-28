import psutil


def services(parameters):
    system_services = list()
    if parameters['targets'] == 'all':
        for service in psutil.win_service_iter():
            system_services.append(service.as_dict())
        return system_services
    else:
        try:
            return psutil.win_service_get(parameters['targets']).as_dict()
        except psutil.NoSuchProcess:
            return {"Error": "Service not found."}
