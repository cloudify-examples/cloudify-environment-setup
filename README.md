
# Cloudify Environment Blueprint

Provisions infrastructure and starts a Cloudify Manager.

_Note: Ignoring a number of factors, the following steps should take 20 - 40 minutes.

To ask a question or report an issue, please use [github issues](https://github.com/cloudify-examples/nodecellar-auto-scale-auto-heal-blueprint/issues) or visit the [Cloudify users groups](https://groups.google.com/forum/#!forum/cloudify-users).


### purpose

Cloudify Manager is designed to work in any environment, whether cloud, baremetal, or a hybrid of the two. This blueprint will deploy the reference environment that is used by other examples.


## pre-requisites

- IaaS Cloud provider and API credentials and sufficient permissions to provision network and compute resources:
  - [AWS Credentials](http://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)
  - [Openstack Credentials](https://docs.openstack.org/user-guide/common/cli-set-environment-variables-using-openstack-rc.html) - *skip step 5 in those instructions -- do not "source" the file*.
  - [Azure Credentials](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-api-authentication)
- [Cloudify CLI](http://docs.getcloudify.org/4.0.0/installation/from-packages/) installed on your computer.


# preparation

Decide how you want to install your manager. There are two options:

* Executing bootstrap (using Cloudify locally to install manager components).

* Using a pre-bootstrapped image. You will find a list of pre-bootstrapped images on [Cloudify's Downloads page](http://cloudify.co/downloads/get_cloudify.html).
  - The current AWS AMIs are listed [here](http://cloudify.co/thank_you_aws_ent) by region.
  - Follow [these instructions](https://docs.openstack.org/user-guide/dashboard-manage-images.html) to upload the [Openstack QCOW image](http://cloudify.co/downloads/get_cloudify.html) to Openstack.
  - There is not currently a pre-bootstrapped image for Azure, so bootstrap is the only option.


# instructions

1. Download and extract this blueprint archive ([link](https://github.com/cloudify-examples/cloudify-environment-blueprint/archive/latest.zip)) to your current working directory.


2. To install your environment's infrastructure, execute one of the example commands below, inserting your account credentials where indicated.

_Note: This command should be run from the same directory in which you extracted the blueprint in the [step 1.](#-instructions)._


#### For AWS run:

```shell
$ cfy install cloudify-environment-blueprint-latest/aws-blueprint.yaml \
    -i aws_secret_access_key=[INSERT_YOUR_AWS_SECRET_KEY] \
    -i aws_access_key_id=[INSERT_YOUR_AWS_ACCESS_KEY] \
    --task-retries=30 --task-retry-interval=5
```


#### For Azure run:

```shell
$ cfy install simple-infrastructure-blueprint/azure-blueprint.yaml \
    -i credentials/simple-infrastructure-blueprint/azure.yaml \
    --task-retries=30 --task-retry-interval=5
```


#### For Openstack run:

```shell
$ cfy install cloudify-environment-blueprint-latest/openstack-blueprint.yaml \
    -i username=[INSERT_YOUR_OPENSTACK_USERNAME] \
    -i password=[INSERT_YOUR_OPENSTACK_PASSWORD] \
    -i tenant_name=[INSERT_YOUR_OPENSTACK_TENANT_NAME] \
    -i auth_url=[INSERT_YOUR_OPENSTACK_V2.0AUTH_URL] \
    -i region=[INSERT_YOUR_OPENSTACK_REGION] \
    -i external_network_name=[INSERT_YOUR_OPENSTACK_EXTERNAL_NETWORK_NAME] \
    -i cloudify_image_id=[INSERT_YOUR_OPENSTACK_CENTOS_OR_CLOUDIFY_IMAGE_ID] \
    -i ubuntu_trusty_id_examples=[INSERT_YOUR_OPENSTACK_UBUNTU_TRUSTY_IMAGE_ID] \
    -i small_openstack_image_flavor=[INSERT_YOUR_OPENSTACK_SMALL_IMAGE_FLAVOR_ID] \
    -i large_openstack_image_flavor=[INSERT_YOUR_OPENSTACK_LARGE_IMAGE_FLAVOR_ID] \
    --task-retries=30 --task-retry-interval=5
```


3. Gather the information you need to configure your manager (or bootstrap and then configure). You can get that information from the `cfy deployments outputs` CLI command.

```shell
$ cfy deployments outputs
```

*The command output should look like this:*

```json
{
  "Bootstrap": {
    "Step0a-Upload-Key": "cat ~/.ssh/cfy-manager-key | ssh -i ~/.ssh/cfy-manager-key cfyuser@**.**.***.*** 'cat >> ~/.ssh/key.pem && chmod 600 ~/.ssh/key.pem'",
    "Step0b-Install-Cloudify-CLI": "ssh -t -i ~/.ssh/cfy-manager-key cfyuser@**.**.***.*** 'sudo rpm -i http://repository.cloudifysource.org/cloudify/4.0.1/sp-release/cloudify-4.0.1~sp.el6.x86_64.rpm'",
    "Step0c-Install-Cloudify-Manager": "ssh -i ~/.ssh/cfy-manager-key cfyuser@**.**.***.*** 'cfy bootstrap --install-plugins /opt/cfy/cloudify-manager-blueprints/simple-manager-blueprint.yaml -i public_ip=13.82.100.239 -i private_ip=10.10.0.4 -i ssh_user=cfyuser -i ssh_key_filename=~/.ssh/key.pem -i agents_user=ubuntu -i ignore_bootstrap_validations=false -i admin_username=admin -i admin_password=admin'"
  },
  "Configuration": {
    "Step1-Initialize-Cloudify-Manager-CLI-Profile": "cfy profiles use -s cfyuser -k ~/.ssh/cfy-manager-key -u admin -p admin -t default_tenant **.**.***.***",
    "Step2-Upload-Openstack-Plugin-Package-Centos": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-azure-plugin/1.4.1/cloudify_azure_plugin-1.4.1-py27-none-linux_x86_64-centos-Core.wgn",
    "Step3-Upload-Diamond-Plugin-Package-Centos": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-centos-Core.wgn",
    "Step4-Upload-Diamond-Plugin-Package-Ubuntu": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-Ubuntu-trusty.wgn",
    "Step5-Create-Azure-Secrets": {
      "First-group": "cfy secrets create -s ********* subscription_id && cfy secrets create  -s ********* tenant_id && cfy secrets create  -s ********* client_id && cfy secrets create  -s i********* client_secret && cfy secrets create  -s eastus location && cfy secrets create  -s pmrg2 mgr_resource_group_name && cfy secrets create  -s pmvn2 mgr_virtual_network_name && cfy secrets create  -s pms02 mgr_subnet_name && cfy secrets create  -s Canonical ubuntu_trusty_image_publisher && cfy secrets create -s UbuntuServer ubuntu_trusty_image_offer && cfy secrets create -s 14.04.4-LTS ubuntu_trusty_image_sku && cfy secrets create -s 14.04.201604060 ubuntu_trusty_image_version && cfy secrets create -s Standard_A0 small_image_size && cfy secrets create -s 'ssh-rsa *********' agent_key_public",
      "Second-group-REMOVE_BACKSLASHES_AROUND_COMMAND_KEEP_DOUBLE_QUOTES": "cfy secrets create agent_key_private -s \"$(<~/.ssh/cfy-agent-key)\""
    }
  },
  "Demo": {
    "Step6-Execute-Nodecellar-Demo": "cfy install https://github.com/cloudify-examples/nodecellar-auto-scale-auto-heal-blueprint/archive/4.0.1.zip -b demo -n azure-haproxy-blueprint.yaml"
  }
}
```


4. Bootstrap

#### Upload an SSH key to the manager VM:

```shell
$ cat ~/.ssh/cfy-manager-key | ssh -i ~/.ssh/cfy-manager-key \
    cfyuser@**.**.***.*** 'cat >> ~/.ssh/key.pem && chmod 600 ~/.ssh/key.pem'
```

_Note: Answer `yes` when prompted.


#### Install the Cloudify CLI on the manager host:

```shell
$ ssh -t -i ~/.ssh/cfy-manager-key \
    cfyuser@**.**.***.*** 'sudo rpm -i \
    http://repository.cloudifysource.org/cloudify/4.0.1/sp-release/cloudify-4.0.1~sp.el6.x86_64.rpm'
```

You will see an output like this:

```shell
You're about to install Cloudify!
Thank you for installing Cloudify!
```


#### Execute bootstrap:

```shell
$ ssh -i ~/.ssh/cfy-manager-key \
    cfyuser@**.**.***.*** 'cfy bootstrap \
    --install-plugins \
    /opt/cfy/cloudify-manager-blueprints/simple-manager-blueprint.yaml \
    -i public_ip=**.**.***.*** -i private_ip=10.10.0.4 -i \
    ssh_user=cfyuser -i ssh_key_filename=~/.ssh/key.pem \
    -i agents_user=ubuntu -i ignore_bootstrap_validations=false \
    -i admin_username=admin -i admin_password=admin'
```

Expect this to take 15-20 minutes.

When you see the following output, the manager is up:

```shell
Bootstrap complete
Manager is up at **.**.***.***
##################################################
Manager password is admin
##################################################
```


5. Configure your manager:

At this stage, it is suggested to wait 5 minutes for all of the services to synchronize. Both bootstrapped and pre-bootstrapped managers need a few moments to stabilize after starting.


#### Initialize the manager CLI profile:

You need to initialize a manager profile in order to control your manager:

```shell
$ cfy profiles use -s cfyuser -k ~/.ssh/cfy-manager-key -u admin -p admin -t default_tenant **.**.***.***
```


#### Upload the plugins for your manager:

_Note: the exact plugins you need to upload vary. The example provided is based on the [Nodecellar Example](https://github.com/cloudify-examples/nodecellar-auto-scale-auto-heal-blueprint/tree/4.0.1) running in Azure._

```shell
$ cfy plugins upload \
    http://repository.cloudifysource.org/cloudify/wagons/cloudify-azure-plugin/1.4.1/cloudify_azure_plugin-1.4.1-py27-none-linux_x86_64-centos-Core.wgn
Uploading plugin http://repository.cloudifysource.org/cloudify/wagons/cloudify-azure-plugin/1.4.1/cloudify_azure_plugin-1.4.1-py27-none-linux_x86_64-centos-Core.wgn...
Plugin uploaded. The plugin's id is 82568a34-f665-4677-af14-16575ea6c0c1
$ cfy plugins upload \
    http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-centos-Core.wgn
Uploading plugin http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-centos-Core.wgn...
Plugin uploaded. The plugin's id is 04efe149-ad8a-4ce1-b840-b0556a6efc18
$ cfy plugins upload \
    http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-Ubuntu-trusty.wgn
Uploading plugin http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-Ubuntu-trusty.wgn...
Plugin uploaded. The plugin's id is adb4c1d5-d2b8-44b6-a4c2-3bef2a78a8f7
```


#### Create your secrets:

Adding secrets to your manager make your deployments more secure. The exact secrets you add also vary by clouds. The below example is based on Azure:

```shell
$ cfy secrets create -s ********* subscription_id && \
    cfy secrets create -s ********* tenant_id && \
    cfy secrets create -s ********* client_id && \
    cfy secrets create -s i********* client_secret && \
    cfy secrets create -s eastus location && \
    cfy secrets create -s pmrg2 mgr_resource_group_name && \
    cfy secrets create -s pmvn2 mgr_virtual_network_name && \
    cfy secrets create -s pms02 mgr_subnet_name && \
    cfy secrets create -s Canonical ubuntu_trusty_image_publisher && \
    cfy secrets create -s UbuntuServer ubuntu_trusty_image_offer && \
    cfy secrets create -s 14.04.4-LTS ubuntu_trusty_image_sku && \
    cfy secrets create -s 14.04.201604060 ubuntu_trusty_image_version && \
    cfy secrets create -s Standard_A0 small_image_size && \
    cfy secrets create -s 'ssh-rsa *********' agent_key_public
Secret `subscription_id` created
Secret `tenant_id` created
Secret `client_id` created
Secret `client_secret` created
Secret `location` created
Secret `mgr_resource_group_name` created
Secret `mgr_virtual_network_name` created
Secret `mgr_subnet_name` created
Secret `ubuntu_trusty_image_publisher` created
Secret `ubuntu_trusty_image_offer` created
Secret `ubuntu_trusty_image_sku` created
Secret `ubuntu_trusty_image_version` created
Secret `small_image_size` created
Secret `agent_key_public` created
$ cfy secrets create agent_key_private -s "$(<~/.ssh/cfy-agent-key)"
Secret `agent_key_private` created
```

*Note that in the last command, the double-quotes are unescaped:*

The deployment output was like this:

```shell
$ cfy secrets create agent_key_private -s \"$(<~/.ssh/cfy-agent-key)\"
```

But you will need to unescape the double quotes so it looks like this:

```shell
$ cfy secrets create agent_key_private -s "$(<~/.ssh/cfy-agent-key)"
```

# Your manager is now ready. Proceed to the example blueprints!*

Start with [Nodecellar Auto-scale Auto-heal](https://github.com/cloudify-examples/nodecellar-auto-scale-auto-heal-blueprint/tree/4.0.1).


6. When you are ready to uninstall your environment, run:

```shell
$ cfy profiles use local
$ cfy uninstall --allow-custom-parameters -p ignore_failure=true --task-retries=30 --task-retry-interval=5
```


# Trouble-shooting

## 502 Bad Gateway

If `cfy profiles use [IP]` fails with this output, trying restarting the VM.

```shell
<head><title>502 Bad Gateway</title></head>
<body bgcolor="white">
<center><h1>502 Bad Gateway</h1></center>
<hr><center>nginx/1.8.0</center>
</body>
</html>
```

