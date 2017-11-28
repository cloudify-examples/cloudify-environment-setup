#!/usr/bin/env python

from cloudify import ctx
from cloudify.exceptions import OperationRetry
from cloudify.state import ctx_parameters as inputs
from cloudify_rest_client.client import CloudifyClient
from cloudify_rest_client.exceptions import CloudifyClientError
from requests.exceptions import ConnectionError
from time import sleep


def get_client(_host, _username, _password, _tenant):
    config = {
        'host': _host,
        'username': _username,
        'password': _password,
        'tenant': _tenant
    }
    return CloudifyClient(**config)


def check_api(
        client_callable,
        arguments=None,
        _progress_handler=None):

    try:
        if isinstance(arguments, dict):
            response = \
                client_callable(**arguments)
        elif arguments is None:
            response = client_callable()
        elif _progress_handler is not None:
            response = \
                client_callable(
                    arguments,
                    progress_callback=_progress_handler)
        else:
            response = \
                client_callable(arguments)
    except ConnectionError as e:
        sleep(5)
        raise OperationRetry('Retrying after error: {0}'.format(str(e)))
    except CloudifyClientError as e:
        if e.status_code == 502:
            sleep(5)
            raise OperationRetry('Retrying after error: {0}'.format(str(e)))
        else:
            sleep(5)
            ctx.logger.error('Ignoring error: {0}'.format(str(e)))
    else:
        sleep(5)
        ctx.logger.debug('Returning response: {0}'.format(response))
        return response
    return None


if __name__ == '__main__':

    # Initialize client.
    manager_admin_user = \
        inputs.get('manager_admin_user', 'admin')
    manager_admin_password = \
        inputs.get('manager_admin_user', 'admin')
    manager_tenant = \
        inputs.get('manager_tenant', 'default_tenant')
    manager_ip = \
        inputs.get('manager_ip')

    client = \
        get_client(
            manager_ip,
            manager_admin_user,
            manager_admin_password,
            manager_tenant)

    if not ctx.node.properties.get('bootstrap'):
        # Wait for it to be ready.
        check_api(client.manager.get_status)
