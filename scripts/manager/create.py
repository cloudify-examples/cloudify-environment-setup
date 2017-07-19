#!/usr/bin/env python

from cloudify import ctx
from fabric.api import put, run, sudo
import tempfile

BOOTSTRAP_COMMAND = \
    'cfy bootstrap ' \
    '{0}' \
    ' -i public_ip={1}' \
    ' -i private_ip={2}' \
    ' -i ssh_user={3}' \
    ' -i ssh_key_filename={4}' \
    ' -i agents_user={5}' \
    ' -i ignore_bootstrap_validations={6}' \
    ' -i admin_username={7}' \
    ' -i admin_password={8}'

instructions = """

Step 1)
  SSH into the manager VM:

{0}

Step 2)
  From within the manager VM, install Cloudify CLI:

{1}

Step 3)
  From within the manager VM, boostrap the Cloudify manager:

{2}

Step 4)
  After bootstrap, exit the VM and initialize the management profile:

cfy profiles use -s {3} -k {4} -u {5} -p {6} -t default_tenant {7}

"""


def create(local_private_key,
           ssh_key_filename,
           rpm_package,
           public_ip,
           private_ip,
           ssh_user='centos',
           agents_user='ubuntu',
           ignore_bootstrap_validations='false',
           admin_username='admin',
           admin_password='admin'):

    if ctx.node.properties.get('bootstrap'):
        put(local_private_key, ssh_key_filename)
        run('chmod 600 {0}'.format(ssh_key_filename))
        ssh_command = 'ssh -i {0} {1}@{2}'.format(local_private_key, ssh_user, public_ip)
        rpm_install_command = 'sudo rpm -i {0}'.format(rpm_package)
        bootstrap_command = \
            BOOTSTRAP_COMMAND.format(
                '/opt/cfy/cloudify-manager-blueprints/simple-manager-blueprint.yaml',
                public_ip,
                private_ip,
                ssh_user,
                ssh_key_filename,
                agents_user,
                ignore_bootstrap_validations,
                admin_username,
                admin_password)
        fd, name = tempfile.mkstemp()
        with open(name, 'w') as out:
            out.write(instructions.format(
                ssh_command,
                rpm_install_command,
                bootstrap_command,
                ssh_user, local_private_key, admin_password, admin_password, public_ip))
        ctx.instance.runtime_properties['instructions_file'] = name
