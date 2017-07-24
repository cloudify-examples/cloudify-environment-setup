#!/usr/bin/env python

from cloudify import ctx
from cloudify.exceptions import OperationRetry
from cloudify.state import ctx_parameters as inputs
from cloudify_rest_client.client import CloudifyClient
from cloudify_rest_client.exceptions import CloudifyClientError
from cloudify_cli.utils import generate_progress_handler
from requests.exceptions import ConnectionError
from time import sleep
import os


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
        if ctx.node.properties.get('create_secrets'):
            # Add secrets.
            for secret in inputs.get('secrets', {}):
                check_api(client.secrets.create, secret)

        if ctx.node.properties.get('upload_plugins'):

            # Upload plugins.
            for plugin in inputs.get('plugin_urls', []):
                ctx.logger.info('plugin: {0}'.format(plugin))
                upload_handler = generate_progress_handler(plugin, '')
                check_api(
                    client.plugins.upload,
                    plugin,
                    _progress_handler=upload_handler)

    if ctx.instance.runtime_properties.get('instructions_file'):
        name = ctx.instance.runtime_properties['instructions_file']

        with open(name, 'a') as out:
            out.write('\n\nStep 5)\n  Create Secrets:\n\n')
            for secret in inputs.get('secrets', {}):
                if isinstance(secret, dict):
                    out.write('\ncfy secrets create {0} -s "{1}"'.format(
                        secret.get('key'), secret.get('value')))
            out.write('\n\nStep 6)\n  Upload Plugins:\n\n')
            for plugin in inputs.get('plugin_urls', []):
                out.write('\ncfy plugins upload {0}'.format(plugin))
        final_path = os.path.join(os.getcwd(), 'instructions.txt')
        if not os.path.exists(final_path):
            os.rename(name, final_path)
        else:
            for n in range(0, 100):
                final_path = \
                    os.path.join(
                        os.getcwd(),
                        'instructions-{0}.txt'.format(str(n))
                    )
                if not os.path.exists(final_path):
                    os.rename(name, final_path)
                    break
            ctx.logger.error('Was not able to write new intruction file.')
        ctx.logger.info('Instructions: {0}'.format(final_path))
        ctx.instance.runtime_properties['final_path'] = final_path
