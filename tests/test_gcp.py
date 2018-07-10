from . import EnvironmentSetupTestBase, eco_utils


class GCPTestBase(EnvironmentSetupTestBase):

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
                'rpm': self.cloudify_rpm_url,
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


class TestGCP432(GCPTestBase):
    pass
