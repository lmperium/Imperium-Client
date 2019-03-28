import psutil


def services(parameters):
    system_services = list()
    if parameters['targets'] == 'all':
        for service in psutil.win_service_iter():
            system_services.append(service.as_dict())
        return system_services
    else:
            for service in parameters['targets']:
                try:
                    s = psutil.win_service_get(service).as_dict()
                    system_services.append(s)
                except psutil.NoSuchProcess:
                    system_services.append({"Error": f"Service {service} not found."})
            return system_services
