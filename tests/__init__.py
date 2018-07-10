# Built-in Imports
import os
import sys

# Cloudify Imports
from ecosystem_tests import (
    PasswordFilter,
    EcosystemTestBase,
    utils as eco_utils)


class EnvironmentSetupTestBase(EcosystemTestBase):

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
    def manager_blueprint_version(self):
        if 'CIRCLE_BRANCH' in os.environ:
            return os.environ['CIRCLE_BRANCH']
        return os.environ.get('MANAGER_BLUEPRINT_VERSION', 'latest')

    @property
    def blueprints_to_check(self):
        return [
            'aws-example-network',
            'azure-example-network',
            'gcp-example-network',
            'openstack-example-network',
        ]

    @property
    def cloudify_rpm_url(self):
        return 'http://repository.cloudifysource.org/cloudify/' \
               '4.3.2/ga-release/cloudify-manager-install-4.3.2ga.rpm'

    @property
    def sensitive_data(self):

        # We need to try returning all of these because
        # we have some common tests in this class.

        try:

            return [
                os.environ['AWS_SECRET_ACCESS_KEY'],
                os.environ['AWS_ACCESS_KEY_ID']
            ]
        except KeyError:
            pass

        try:
            return [
                os.environ['GCP_CERT_URL'],
                os.environ['GCP_EMAIL'],
                os.environ['GCP_CLIENT_ID'],
                os.environ['GCP_PRIVATE_PROJECT_ID'],
                os.environ['GCP_PRIVATE_KEY_ID'],
                os.environ['GCP_PRIVATE_KEY'],
                os.environ['GCP_PRIVATE_KEY'].decode('string_escape')
            ]
        except KeyError:
            pass

        try:
            return [
                os.environ['AZURE_SUB_ID'],
                os.environ['AZURE_TEN_ID'],
                os.environ['AZURE_CLI_ID'],
                os.environ['AZURE_CLI_SE']
            ]
        except KeyError:
            raise

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
