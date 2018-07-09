

# Cloudify Environment Setup

To ask a question or report an issue, please visit the [Cloudify users groups](https://groups.google.com/forum/#!forum/cloudify-users) or report an issue using [github issues](https://github.com/cloudify-examples/cloudify-environment-setup/issues).


## Purpose

* Bring up a basic network.
* Install a Cloudify Manager:
  * Setup the default and external management networks.
* Configure the Cloudify Manager:
  * Upload basic plugins.
  * Create secrets.

This blueprint is intended to be executed from `cfy local`.


### Pre-requisites

- IaaS Cloud provider and API credentials and sufficient permissions to provision network and compute resources:
  - [AWS Credentials](http://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)
  - [Openstack Credentials](https://docs.openstack.org/user-guide/common/cli-set-environment-variables-using-openstack-rc.html) - *skip step 5 in those instructions -- do not "source" the file*.
  - [Azure Credentials](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-api-authentication)
  - [GCP Credentials](https://cloud.google.com/docs/authentication/getting-started)
- A virtual environment application such as [virtualenv](https://virtualenv.pypa.io/en/stable/) installed on your computer.
- [Cloudify CLI](http://docs.getcloudify.org/4.3.0/installation/from-packages/) installed in a virtual environment.


## Environment Installation Steps

Once you have decided on a Manager installation method, you can proceed on the path of execution:

1. Install [Cloudify CLI](http://docs.getcloudify.org/4.3.0/installation/from-packages/). Make sure that your CLI is using a local [profile](http://docs.getcloudify.org/4.3.0/cli/profiles/). (You must have executed `cfy profiles use local` in your shell.

2. Download and extract this blueprint archive ([link](https://github.com/cloudify-examples/cloudify-environment-setup/archive/latest.zip)) to your current working directory. You will create an inputs yaml file. Examples are provided in the `inputs` directory already if you prefer.

3. To install your environment's infrastructure, execute one of the example commands below, inserting your account credentials in the _*.yaml_ file located in the _inputs_ directory for your IaaS.

_Note: This command should be run from the same directory in which you extracted the blueprint in the previous step. If it stops after installing plugins (some users have noted this issue), run the command again without '--install-plugins' to complete the setup._

For AWS run:

```shell
$ cfy install cloudify-environment-setup-latest/aws.yaml -i cloudify-environment-setup-latest/inputs/aws.yaml --install-plugins --task-retries=30 --task-retry-interval=5
```

For Azure run:

```shell
$ cfy install cloudify-environment-setup-latest/azure.yaml -i cloudify-environment-setup-latest/inputs/azure.yaml --install-plugins --task-retries=30 --task-retry-interval=5
```

For Openstack run:

```shell
$ cfy install cloudify-environment-setup-latest/openstack.yaml -i cloudify-environment-setup-latest/inputs/openstack.yaml --install-plugins --task-retries=30 --task-retry-interval=5
```

For GCP run:

```shell
$ cfy install cloudify-environment-setup-latest/gcp.yaml -i cloudify-environment-setup-latest/inputs/gcp.yaml --install-plugins --task-retries=30 --task-retry-interval=5
```


## Environment Teardown Steps

When you are ready to uninstall your environment, run:

```shell
$ cfy profiles use local
$ cfy uninstall --allow-custom-parameters -p ignore_failure=true --task-retries=30 --task-retry-interval=5 -b cloudify-environment-setup-latest

```
