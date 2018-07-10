from . import EnvironmentSetupTestBase, eco_utils


class AzureTestBase(EnvironmentSetupTestBase):

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
                'rpm': self.cloudify_rpm_url,
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

class TestAzure432(AzureTestBase):
    pass
