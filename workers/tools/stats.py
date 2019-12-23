from workers.celery import celery_app


def _get_inspector_proxy(worker_name=None):

    if worker_name is None:
        i = celery_app.control.inspect()
    else:
        i = celery_app.control.inspect(worker_name)

    return i


def get_registered_tasks_list():

    _inspector = _get_inspector_proxy()

    return _inspector.registered()


def get_active_tasks_list():

    _inspector = _get_inspector_proxy()

    return _inspector.active()


def get_registered_tasks_list():

    _inspector = _get_inspector_proxy()

    return _inspector.registered()


def get_scheduled_tasks_list():

    _inspector = _get_inspector_proxy()

    return _inspector.scheduled()