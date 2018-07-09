# Built-in Imports
import os
import sys

# Cloudify Imports
from ecosystem_tests import (
    PasswordFilter,
    EcosystemTestBase,
    utils as eco_utils)


class TestAWS(EcosystemTestBase):

    def setUp(self):
        if self.password not in self.sensitive_data:
            self.sensitive_data.append(self.password)
        sys.stdout = PasswordFilter(self.sensitive_data, sys.stdout)
        sys.stderr = PasswordFilter(self.sensitive_data, sys.stderr)
        self.cfy_local = self.setup_cfy_local()
        os.environ['AWS_DEFAULT_REGION'] = self.inputs.get('ec2_region_name')
        if 'ECOSYSTEM_SESSION_MANAGER_IP' in os.environ:
            self.manager_ip = \
                os.environ['ECOSYSTEM_SESSION_MANAGER_IP']
        else:
            self.install_manager()
            self.initialize_manager_profile()

    @property
    def node_type_prefix(self):
        return 'cloudify.nodes.aws'

    @property
    def plugin_mapping(self):
        return 'awssdk'

    @property
    def blueprint_file_name(self):
        return 'aws.yaml'

    @property
    def external_id_key(self):
        return 'aws_resource_id'

    @property
    def server_ip_property(self):
        return 'ip'

    @property
    def sensitive_data(self):
        return [
            os.environ['AWS_SECRET_ACCESS_KEY'],
            os.environ['AWS_ACCESS_KEY_ID']
        ]

    @property
    def inputs(self):
        try:
            return {
                'password': os.environ['ECOSYSTEM_SESSION_PASSWORD'],
                'ec2_region_name': 'eu-central-1',
                'ec2_region_endpoint': 'ec2.eu-central-1.amazonaws.com',
                'availability_zone': 'eu-central-1b',
                'aws_secret_access_key': os.environ['AWS_SECRET_ACCESS_KEY'],
                'aws_access_key_id': os.environ['AWS_ACCESS_KEY_ID']
            }
        except KeyError:
            raise

    @property
    def blueprints_to_check(self):
        return [
            'aws-example-network',
            'azure-example-network',
            'gcp-example-network',
            'openstack-example-network',
        ]

    @property
    def secrets_to_check(self):
        return [
            'agent_key_private',
            'agent_key_public',
            'centos_core_image',
            'ubuntu_trusty_image',
            'availability_zone',
            'private_subnet_id',
            'public_subnet_id',
            'vpc_id',
            'ec2_region_endpoint',
            'ec2_region_name',
            'aws_secret_access_key',
            'aws_access_key_id',
        ]

    def test_secrets(self):
        for secret in self.secrets_to_check:
            self.assertIsNotNone(eco_utils.get_secrets(secret))

    def test_blueprints(self):
        for blueprint in self.blueprints_to_check:
            try:
                eco_utils.get_client_response(
                    'blueprints',
                    'get',
                    {'blueprint_id': blueprint})
            except:
                self.fail(
                    'Blueprint {0} does not exist'.format(blueprint))

    def test_network_deployment(self):
        self.addCleanup(self.cleanup_deployment, 'aws-example-network')
        # Create Deployment (Blueprint already uploaded.)
        if eco_utils.create_deployment('aws-example-network'):
            raise Exception(
                'Deployment aws-example-network failed.')
        # Install Deployment.
        if eco_utils.execute_install('aws-example-network'):
            raise Exception(
                'Install aws-example-network failed.')
        if eco_utils.execute_uninstall('aws-example-network'):
            raise Exception('Uninstall aws-example-network failed.')


class TestAzure(EcosystemTestBase):

    def setUp(self):
        if self.password not in self.sensitive_data:
            self.sensitive_data.append(self.password)
        sys.stdout = PasswordFilter(self.sensitive_data, sys.stdout)
        sys.stderr = PasswordFilter(self.sensitive_data, sys.stderr)
        self.cfy_local = self.setup_cfy_local()
        if 'ECOSYSTEM_SESSION_MANAGER_IP' in os.environ:
            self.manager_ip = \
                os.environ['ECOSYSTEM_SESSION_MANAGER_IP']
        else:
            self.install_manager()
            self.initialize_manager_profile()

    @property
    def node_type_prefix(self):
        return 'cloudify.azure.nodes'

    @property
    def plugin_mapping(self):
        return 'pkg'

    @property
    def blueprint_file_name(self):
        return 'azure.yaml'

    @property
    def external_id_key(self):
        return 'public_ip'

    @property
    def server_ip_property(self):
        return 'cloudify_host'

    @property
    def sensitive_data(self):
        return [
            os.environ['AZURE_SUB_ID'],
            os.environ['AZURE_TEN_ID'],
            os.environ['AZURE_CLI_ID'],
            os.environ['AZURE_CLI_SE']
        ]

    @property
    def inputs(self):
        try:
            return {
                'password': self.password,
                'location': 'westus',
                'resource_prefix': 'ecotest',
                'resource_suffix': self.application_prefix,
                'subscription_id': os.environ['AZURE_SUB_ID'],
                'tenant_id': os.environ['AZURE_TEN_ID'],
                'client_id': os.environ['AZURE_CLI_ID'],
                'client_secret': os.environ['AZURE_CLI_SE'],
                'large_image_size': 'Standard_H8m'
            }
        except KeyError:
            raise

    @property
    def blueprints_to_check(self):
        return [
            'aws-example-network',
            'azure-example-network',
            'gcp-example-network',
            'openstack-example-network',
        ]

    @property
    def secrets_to_check(self):
        return [
            'agent_key_private',
            'agent_key_public',
            'azure_location',
            'large_image_size',
            'small_image_size',
            'centos_core_image_version',
            'centos_core_image_sku',
            'centos_core_image_offer',
            'centos_core_image_publisher',
            'centos_core_image_offer',
            'centos_core_image_publisher',
            'ubuntu_trusty_image_version',
            'centos_core_image_publisher',
            'ubuntu_trusty_image_version',
            'ubuntu_trusty_image_sku',
            'ubuntu_trusty_image_offer',
            'ubuntu_trusty_image_publisher',
            'mgr_subnet_name',
            'mgr_virtual_network_name',
            'mgr_resource_group_name',
            'azure_location',
            'azure_client_secret',
            'azure_client_id',
            'azure_tenant_id',
            'azure_subscription_id',
            'location',
            'client_secret',
            'client_id',
            'tenant_id',
            'subscription_id',
        ]

    def test_network_deployment(self):
        self.addCleanup(self.cleanup_deployment, 'azure-example-network')
        # Create Deployment (Blueprint already uploaded.)
        _inputs = {
            'resource_prefix': 'ecotestnet',
            'resource_suffix': self.application_prefix
        }
        if eco_utils.create_deployment(
                'azure-example-network',
                inputs=_inputs):
            raise Exception(
                'Deployment azure-example-network failed.')
        # Install Deployment.
        if eco_utils.execute_install('azure-example-network'):
            raise Exception(
                'Install azure-example-network failed.')
        if eco_utils.execute_uninstall('azure-example-network'):
            raise Exception('Uninstall azure-example-network failed.')

    def test_blueprints(self):
        for blueprint in self.blueprints_to_check:
            try:
                eco_utils.get_client_response(
                    'blueprints',
                    'get',
                    {'blueprint_id': blueprint})
            except:
                self.fail(
                    'Blueprint {0} does not exist'.format(blueprint))

    def test_secrets(self):
        for secret in self.secrets_to_check:
            self.assertIsNotNone(eco_utils.get_secrets(secret))


class TestGCP(EcosystemTestBase):

    def setUp(self):
        if self.password not in self.sensitive_data:
            self.sensitive_data.append(self.password)
        sys.stdout = PasswordFilter(self.sensitive_data, sys.stdout)
        sys.stderr = PasswordFilter(self.sensitive_data, sys.stderr)
        self.cfy_local = self.setup_cfy_local()
        if 'ECOSYSTEM_SESSION_MANAGER_IP' in os.environ:
            self.manager_ip = \
                os.environ['ECOSYSTEM_SESSION_MANAGER_IP']
        else:
            self.install_manager()
            self.initialize_manager_profile()

    @property
    def node_type_prefix(self):
        return 'cloudify.gcp.nodes'

    @property
    def plugin_mapping(self):
        return 'gcp_plugin'

    @property
    def blueprint_file_name(self):
        return 'gcp.yaml'

    @property
    def external_id_key(self):
        return 'natIP'

    @property
    def server_ip_property(self):
        return 'cloudify_host'

    @property
    def sensitive_data(self):
        return [
            os.environ['GCP_CERT_URL'],
            os.environ['GCP_EMAIL'],
            os.environ['GCP_CLIENT_ID'],
            os.environ['GCP_PRIVATE_PROJECT_ID'],
            os.environ['GCP_PRIVATE_KEY_ID'],
            os.environ['GCP_PRIVATE_KEY'].decode('string_escape')
        ]

    @property
    def inputs(self):
        try:
            return {
                'password': self.password,
                'region': 'europe-west1',
                'zone': 'europe-west1-b',
                'resource_prefix': 'trammell',
                'client_x509_cert_url': os.environ['GCP_CERT_URL'],
                'client_email': os.environ['GCP_EMAIL'],
                'client_id': os.environ['GCP_CLIENT_ID'],
                'project_id': os.environ['GCP_PRIVATE_PROJECT_ID'],
                'private_key_id': os.environ['GCP_PRIVATE_KEY_ID'],
                'private_key':
                    os.environ['GCP_PRIVATE_KEY'].decode('string_escape'),
            }
        except KeyError:
            raise

    @property
    def blueprints_to_check(self):
        return [
            'aws-example-network',
            'azure-example-network',
            'gcp-example-network',
            'openstack-example-network',
        ]

    @property
    def secrets_to_check(self):
        return [
            'agent_key_private',
            'agent_key_public',
            'small_instance_type',
            'centos_core_image',
            'ubuntu_trusty_image',
            'private_subnetwork_name',
            'management_subnetwork_name',
            'management_network_name',
            'gcp_region',
            'gcp_zone',
            'gcp_private_key',
            'gcp_private_key_id',
            'gcp_project_id',
            'gcp_client_id',
            'gcp_client_email',
            'gcp_client_x509_cert_url',
            'region',
            'zone',
            'private_key',
            'private_key_id',
            'project_id',
            'client_id',
            'client_email',
            'client_x509_cert_url'
        ]

    def get_manager_ip(self):
        for instance in self.node_instances:
            if instance.node_id == self.server_ip_property:
                props = instance.runtime_properties
                nic = props['networkInterfaces'][0]
                return nic['accessConfigs'][0][self.external_id_key]
        raise Exception('No manager IP found.')

    def test_blueprints(self):
        for blueprint in self.blueprints_to_check:
            try:
                eco_utils.get_client_response(
                    'blueprints',
                    'get',
                    {'blueprint_id': blueprint})
            except:
                self.fail(
                    'Blueprint {0} does not exist'.format(blueprint))

    def test_secrets(self):
        for secret in self.secrets_to_check:
            self.assertIsNotNone(eco_utils.get_secrets(secret))

    def test_network_deployment(self):
        _inputs = {
            'resource_prefix': 'ecotestnet',
            'resource_suffix': self.application_prefix
        }
        self.addCleanup(self.cleanup_deployment, 'gcp-example-network')
        # Create Deployment (Blueprint already uploaded.)
        if eco_utils.create_deployment(
                'gcp-example-network',
                inputs=_inputs):
            raise Exception(
                'Deployment gcp-example-network failed.')
        # Install Deployment.
        if eco_utils.execute_install('gcp-example-network'):
            raise Exception(
                'Install gcp-example-network failed.')
        if eco_utils.execute_uninstall('gcp-example-network'):
            raise Exception('Uninstall gcp-example-network failed.')
