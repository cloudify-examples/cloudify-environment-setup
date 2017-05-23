
# Cloudify Environment Blueprint

Provisions infrastructure and starts a Cloudify Manager.


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

* Executing bootstrap (using Cloudify locally to install manager components). If you want to bootstrap, continue to the instructions for your cloud. After you deploy your cloud environment, you will find additional steps (Step0a, Step0b, and Step0c) in the deployment outputs.
  - [AWS](#aws-instructions)
  - [Openstack](#openstack-instructions)
  - [Azure](#azure-instructions)


* Using a pre-bootstrapped image. You will find a list of pre-bootstrapped images on [Cloudify's Downloads page](http://cloudify.co/downloads/get_cloudify.html).
  - The current AWS AMIs are listed [here](http://cloudify.co/thank_you_aws_ent) by region.
  - Follow [these instructions](https://docs.openstack.org/user-guide/dashboard-manage-images.html) to upload the [Openstack QCOW image](http://cloudify.co/downloads/get_cloudify.html) to Openstack.


# aws instructions

1. Download and extract this blueprint archive ([link](https://github.com/cloudify-examples/cloudify-environment-blueprint/archive/latest.zip)) to your current working directory.

2. Install the infrastructure and insert your AWS Account Keys where indicated in the example command below.

_Note: This command should be run from the same directory in which you extracted the blueprint in the previous step._

```shell
$ cfy install cloudify-environment-blueprint-latest/aws-blueprint.yaml \
    -i aws_secret_access_key=[INSERT_YOUR_AWS_SECRET_KEY] \
    -i aws_access_key_id=[INSERT_YOUR_AWS_ACCESS_KEY] \
    --task-retries=30 --task-retry-interval=5
```


3. Show the outputs, and follow the instructions to configure your manager and run the demo application.

```shell
$ cfy deployments outputs
```

_Advice: Wait a couple minutes after the installation has succeeded to run these commands._

_Note: Your example output should look like this:_

```json
{
  "Configure-Manager-and-Run-Example": {
    "Step1-Initialize-Cloudify-Manager-CLI-Profile": "cfy profiles use -s centos -k ~/.ssh/cfy-manager-key.pem -u admin -p admin -t default_tenant **********",
    "Step2-Upload-AWS-Plugin-Package-Centos": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-aws-plugin/1.4.4/cloudify_aws_plugin-1.4.4-py27-none-linux_x86_64-centos-Core.wgn",
    "Step3-Upload-Diamond-Plugin-Package-Centos": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-centos-Core.wgn",
    "Step4-Upload-Diamond-Plugin-Package-Ubuntu": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-Ubuntu-trusty.wgn",
    "Step5-Create-AWS-Secrets": "cfy secrets create -s ********** aws_access_key_id && cfy secrets create  -s ********** aws_secret_access_key",
    "Step6-Execute-Nodecellar-Demo": "cfy install https://github.com/cloudify-examples/nodecellar-auto-scale-auto-heal-blueprint/archive/4.0.zip -b demo -n aws-haproxy-blueprint.yaml -i ec2_region_name=us-east-1 -i ec2_region_endpoint=ec2.us-east-1.amazonaws.com -i vpc_id=********** -i public_subnet_id=********** -i private_subnet_id=********** -i availability_zone=us-east-1e -i ami=ami-772aa961"
  }
}
```

_Note: In rare cases, the VM will not provision correctly and you may see this response to the ```cfy profiles use...``` command:_

```shell
<head><title>502 Bad Gateway</title></head>
<body bgcolor="white">
<center><h1>502 Bad Gateway</h1></center>
<hr><center>nginx/1.8.0</center>
</body>
</html>
```

If that is the case, restart the Manager VM.


# openstack instructions

1. Download and extract this blueprint archive ([link](https://github.com/cloudify-examples/cloudify-environment-blueprint/archive/latest.zip)) to your current working directory.

2. Install the infrastructure and insert your Openstack credentials where indicated in the example command below.

_Note: This command should be run from the same directory in which you extracted the blueprint in the previous step._

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


3. Show the outputs, and follow the instructions to configure your manager and run the demo application.

```shell
$ cfy deployments outputs
```

_Advice: Wait a couple minutes after the installation has succeeded to run these commands._

_Note: Your example output should look like this:_

```json
{
  "Configure-Manager-and-Run-Example": {
    "Step0a-Upload-Key": "cat ~/.ssh/cfy-manager-key.pem | ssh -i ~/.ssh/cfy-manager-key.pem centos@***.***.***.*** 'cat >> ~/.ssh/key.pem && chmod 600 ~/.ssh/key.pem'",
    "Step0b-Install-Cloudify-CLI": "ssh -t -i ~/.ssh/cfy-manager-key.pem centos@***.***.***.*** 'sudo rpm -i http://repository.cloudifysource.org/cloudify/4.0.1/sp-release/cloudify-4.0.1~sp.el6.x86_64.rpm'",
    "Step0c-Install-Cloudify-Manager": "ssh -i ~/.ssh/cfy-manager-key.pem centos@***.***.***.*** 'cfy bootstrap --install-plugins /opt/cfy/cloudify-manager-blueprints/simple-manager-blueprint.yaml -i public_ip=***.***.***.*** -i private_ip=***.***.***.*** -i ssh_user=centos -i ssh_key_filename=~/.ssh/key.pem -i agents_user=ubuntu -i ignore_bootstrap_validations=false -i admin_username=admin -i admin_password=admin'",
    "Step1-Initialize-Cloudify-Manager-CLI-Profile": "cfy profiles use -s centos -k ~/.ssh/cfy-manager-key.pem -u admin -p admin -t default_tenant ***.***.***.***",
    "Step2-Upload-Openstack-Plugin-Package-Centos": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-openstack-plugin/2.0.1/cloudify_openstack_plugin-2.0.1-py27-none-linux_x86_64-centos-Core.wgn",
    "Step3-Upload-Diamond-Plugin-Package-Centos": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-centos-Core.wgn",
    "Step4-Upload-Diamond-Plugin-Package-Ubuntu": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-Ubuntu-trusty.wgn",
    "Step5-Create-Openstack-Secrets": "cfy secrets create -s ******* keystone_username && cfy secrets create  -s ******* keystone_password && cfy secrets create  -s ******* keystone_tenant_name && cfy secrets create -s ******* keystone_url",
    "Step6-Execute-Nodecellar-Demo": "cfy install https://github.com/cloudify-examples/nodecellar-auto-scale-auto-heal-blueprint/archive/4.0.zip -b demo -n openstack-haproxy-blueprint.yaml -i region=RegionOne -i external_network_name=GATEWAY_NET -i router_name=network0_router -i public_network_name=network0 -i private_network_name=network1 -i public_subnet_name=network0_subnet -i private_subnet_name=network1_subnet -i image=e41430f7-9131-495b-927f-e7dc4b8994c8 -i flavor=1"
  }
}
```


# azure instructions

1. Download and extract this blueprint archive ([link](https://github.com/cloudify-examples/cloudify-environment-blueprint/archive/latest.zip)) to your current working directory.

2. Install the infrastructure and insert your Azure credentials where indicated in the example command below.

_Note: This command should be run from the same directory in which you extracted the blueprint in the previous step._

```shell
$ cfy install simple-infrastructure-blueprint/azure-blueprint.yaml \
    -i credentials/simple-infrastructure-blueprint/azure.yaml \
    --task-retries=30 --task-retry-interval=5
```


3. Show the outputs, and follow the instructions to configure your manager and run the demo application.

```shell
$ cfy deployments outputs
```

_Advice: Wait a couple minutes after the installation has succeeded to run these commands._

_Note: Your example output should look like this:_

```json
{
  "Configure-Manager-and-Run-Example": {
    "Step0a-Upload-Key": "cat ~/.ssh/cfy-manager-key | ssh -i ~/.ssh/cfy-manager-key cfyuser@***.***.***.*** 'cat >> ~/.ssh/key.pem && chmod 600 ~/.ssh/key.pem'",
    "Step0b-Install-Cloudify-CLI": "ssh -t -i ~/.ssh/cfy-manager-key cfyuser@***.***.***.*** 'sudo rpm -i http://repository.cloudifysource.org/cloudify/4.0.1/sp-release/cloudify-4.0.1~sp.el6.x86_64.rpm'",
    "Step0c-Install-Cloudify-Manager": "ssh -i ~/.ssh/cfy-manager-key cfyuser@***.***.***.*** 'cfy bootstrap --install-plugins /opt/cfy/cloudify-manager-blueprints/simple-manager-blueprint.yaml -i public_ip=40.71.173.208 -i private_ip=10.10.0.4 -i ssh_user=cfyuser -i ssh_key_filename=~/.ssh/key.pem -i agents_user=ubuntu -i ignore_bootstrap_validations=false -i admin_username=admin -i admin_password=admin'",
    "Step1-Initialize-Cloudify-Manager-CLI-Profile": "cfy profiles use -s cfyuser -k ~/.ssh/cfy-manager-key -u admin -p admin -t default_tenant ***.***.***.***",
    "Step2-Upload-Azure-Plugin-Package-Centos": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-azure-plugin/1.4.1/cloudify_azure_plugin-1.4.1-py27-none-linux_x86_64-centos-Core.wgn",
    "Step3-Upload-Diamond-Plugin-Package-Centos": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-centos-Core.wgn",
    "Step4-Upload-Diamond-Plugin-Package-Ubuntu": "cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.5/cloudify_diamond_plugin-1.3.5-py27-none-linux_x86_64-Ubuntu-trusty.wgn",
    "Step5-Create-Azure-Secrets": "cfy secrets create -s ***************** subscription_id && cfy secrets create  -s ***************** tenant_id && cfy secrets create  -s ***************** client_id && cfy secrets create  -s ***************** client_secret",
    "Step6-Execute-Nodecellar-Demo": "cfy install https://github.com/cloudify-examples/nodecellar-auto-scale-auto-heal-blueprint/archive/4.0.zip -b demo -n azure-haproxy-blueprint.yaml -i location=eastus -i mgr_resource_group_name=******* -i mgr_virtual_network_name=******* -i mgr_subnet_name=******* -i vm_os_username_public_key_data='************' -i cloudify_manager_agent_key_path=/home/cfyuser/.ssh/key.pem"
  }
}
```

# uninstall instructions

1. To uninstall the demo app, run:

```shell
$ cfy uninstall demo --allow-custom-parameters -p ignore_failure=true
```


2. To uninstall the example environment, run:

```shell
$ cfy profiles use local
$ cfy uninstall --allow-custom-parameters -p ignore_failure=true --task-retries=30 --task-retry-interval=5
```
