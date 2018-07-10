from . import EnvironmentSetupTestBase, eco_utils


class AWSTestbase(EnvironmentSetupTestBase):

    def setUp(self):
        os.environ['AWS_DEFAULT_REGION'] = \
            self.inputs.get('ec2_region_name')
        super(TestAWS432, self).setUp()

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
                'rpm': self.cloudify_rpm_url,
                'password': os.environ['ECOSYSTEM_SESSION_PASSWORD'],
                'ec2_region_name': 'ap-southeast-1',
                'ec2_region_endpoint': 'ec2.ap-southeast-1.amazonaws.com',
                'availability_zone': 'ap-southeast-1b',
                'aws_secret_access_key': os.environ['AWS_SECRET_ACCESS_KEY'],
                'aws_access_key_id': os.environ['AWS_ACCESS_KEY_ID']
            }
        except KeyError:
            raise

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

class TestAWS432(AWSTestbase):
    pass
