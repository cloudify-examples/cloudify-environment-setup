
# Cloudify Environment Setup

_Note: Without bootstrap, deployment should take 5 minutes. With bootstrap, up to 40 minutes._

To ask a question or report an issue, please use [github issues](https://github.com/cloudify-examples/cloudify-environment-setup/issues) or visit the [Cloudify users groups](https://groups.google.com/forum/#!forum/cloudify-users).


# Purpose

This blueprint sets up a reference environment for executing the Cloudify Examples. When you execute this blueprint, you will create all the networks, routes, security groups, NICs, VMs, plugins, and secrets that you will need to run the other Cloudify Examples.


### Pre-requisites

- IaaS Cloud provider and API credentials and sufficient permissions to provision network and compute resources:
  - [AWS Credentials](http://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)
  - [Openstack Credentials](https://docs.openstack.org/user-guide/common/cli-set-environment-variables-using-openstack-rc.html) - *skip step 5 in those instructions -- do not "source" the file*.
  - [Azure Credentials](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-api-authentication)
- A virtual environment application such as [virtualenv](https://virtualenv.pypa.io/en/stable/) installed on your computer.
- [Cloudify CLI](http://docs.getcloudify.org/4.1.0/installation/from-packages/) installed in a virtual environment.


## Infrastructure

When you execute the blueprint, you will provision the following resources in your cloud:

* Common Infrastructure
  * manager_key: An SSH key pair used to connect to the Cloudify Manager.
  * agent_key: An SSH key pair used by the Cloudify Manager to connect other VMs that it creates.
  * ManagerSetup: see ManagerSetup.

* AWS Infrastructure:
  * subnet0_nic_eip0
  * subnet0_nic_eip1
  * vpc
  * internet_gateway
  * subnet0
  * subnet1
  * nat_instance_security_group
  * cloudify_security_group
  * subnet0_nic0
  * subnet0_nic1
  * nat_instance
  * route_table0
  * route_table1
  * cloudify_host_cloud_config
  * cloudify_host

* Azure Infrastructure:
  * resource_group
  * storage_account
  * availability_set
  * subnet0_nic_ip
  * virtual_network
  * security_group
  * subnet0
  * subnet1
  * subnet0_nic_ip_configuration
  * subnet1_nic_ip_configuration
  * subnet0_nic
  * subnet1_nic
  * cloudify_host

* Openstack Infrastructure:
  * external_network
  * network0_subnet_port_fip
  * network0
  * network1
  * network0_router
  * network0_subnet
  * network1_subnet
  * cloudify_security_group
  * network0_subnet_port
  * network1_subnet_port
  * cloudify_host_cloud_config
  * cloudify_host


#### Secrets


* Common Secrets:
  * agent_key_private
  * agent_key_public

**Bootstrap**

* AWS Secrets:
  * vpc_id: This is the ID of the vpc. The same vpc that your manager is attached to.
  * private_subnet_id: This is the ID of a subnet that does not have inbound internet access on the vpc. Outbound internet access is required to download the requirements.  It must be on the same vpc designated by VPC_ID.
  * public_subnet_id: This is the ID of a subnet that does have internet access (inbound and outbound).  It must be on the same vpc designated by VPC_ID.
  * availability_zone: The availability zone that you want your instances created in. This must be the same as your public_subnet_id and private_subnet_id.
  * [ec2_region_endpoint](http://docs.aws.amazon.com/general/latest/gr/rande.html): The AWS region endpint, such as ec2.us-east-1.amazonaws.com.
  * ec2_region_name: The AWS region name, such as ec2_region_name.
  * aws_secret_access_key: Your AWS Secret Access Key. See [here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration) for more info. This may not be provided as an environment variable. The string must be set as a secret.
  * aws_access_key_id: Your AWS Access Key ID. See [here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration) for more info. This may not be provided as an environment variable. The string must be set as a secret.


* Azure Secrets:
  * location: See [here](https://azure.microsoft.com/en-us/regions/).
  * mgr_virtual_network_name: This is the name of the virtual network that your manager is attached to.
  * mgr_subnet_name: The is the name of the subnet that your manager is attached to.
  * mgr_resource_group_name: This the resource group that your manager is sitting in.
  * client_secret: Your Azure Service Principal password. See [here](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-authenticate-service-principal-cli#create-service-principal-with-password).
  * client_id: Your Azure Service Principal appId. See [here](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-authenticate-service-principal-cli#create-service-principal-with-password).
  * tenant_id: Your Azure Service Principal tenant. See [here](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-authenticate-service-principal-cli#create-service-principal-with-password).
  * subscription_id: Your Azure subscription ID.


* Openstack Secrets:
  * external_network_name: This is the network on your Openstack that represents the internet gateway network.
  * public_network_name: An openstack network. (Inbound is expected, outbound is required.)
  * public_subnet_name: A subnet on the public network.
  * private_network_name: An openstack network. (Inbound is not expected, outbound is required.)
  * private_subnet_name: A subnet on the network. (Inbound is not expected, outbound is required.)
  * router_name: This is a router that is attached to your Subnets designated in the secrets public_subnet_name and private_subnet_name.
  * region: Your Keystone V2 region.
  * keystone_url: Your Keystone V2 auth URL.
  * keystone_tenant_name: Your Keystone V2 tenant name.
  * keystone_password: Your Keystone V2 password.
  * keystone_username:Your Keystone V2 username.

_Note: This command should be run from the same directory in which you extracted the blueprint in the previous step._

## Preparation

You must choose one of two installation paths. These are:

1. Bootstrap Cloudify. This is available regardless of cloud provider/hosting provider/IaaS. *Slower*.
2. Use a pre-baked Cloudify image. This is currently only available in Openstack and AWS. *Faster*.


**Bootstrap**

To execute bootstrap, add "bootstrap: True" as a single line to your "*.yaml" file. This is the default already in the sample input files.

**Using a pre-baked image.**

You will find a list of pre-bootstrapped images on [Cloudify's Downloads page](http://cloudify.co/download).

  - AWS: AMIs are listed in the "aws-blueprint.yaml" under the `cloudify_ami` input.
    You may also find links [here](http://cloudify.co/thank_you_aws_ent).
    Also, change the "bootstrap: True" to "False" in your inputs file.
  - Openstack: Follow [these instructions](https://docs.openstack.org/user-guide/dashboard-manage-images.html) to upload the [Openstack QCOW image](https://repository.cloudifysource.org/cloudify/4.1.1/ga-release/cloudify-enterprise-manager-4.1.1ga.qcow2) to Openstack.
    You will also need to find the correct values for cloudify_image, centos_core_image, ubuntu_trusty_image, small_image_flavor, large_image_flavor. Ask your Openstack Admin for more info on these.
  - Azure: There is not currently a pre-bootstrapped image for Azure, so bootstrap is the only option.



## Environment Installation Steps

Once you have decided on a Manager installation method, you can proceed on the path of execution:

1. Install [Cloudify CLI](http://docs.getcloudify.org/4.1.0/installation/from-packages/). Make sure that your CLI is using a local [profile](http://docs.getcloudify.org/4.1.0/cli/profiles/). (You must have executed `cfy profiles use local` in your shell.

2. Download and extract this blueprint archive ([link](https://github.com/cloudify-examples/cloudify-environment-setup/archive/latest.zip)) to your current working directory. You will create an inputs yaml file. Examples are provided in the `inputs` directory already if you prefer.

3. To install your environment's infrastructure, execute one of the example commands below, inserting your account credentials in the _*.yaml_ file located in the _inputs_ directory for your IaaS.

_Note: This command should be run from the same directory in which you extracted the blueprint in the previous step. If it stops after installing plugins (some users have noted this issue), run the command again without '--install-plugins' to complete the setup._

For AWS run:

```shell
$ cfy install cloudify-environment-setup-latest/aws-blueprint.yaml -i cloudify-environment-setup-latest/inputs/aws.yaml --install-plugins
```

For Azure run:

```shell
$ cfy install cloudify-environment-setup-latest/azure-blueprint.yaml -i cloudify-environment-setup-latest/inputs/azure.yaml --install-plugins
```

For Openstack run:

```shell
$ cfy install cloudify-environment-setup-latest/openstack-blueprint.yaml -i cloudify-environment-setup-latest/inputs/openstack.yaml --install-plugins
```

_Only run the below Manager Setup Steps if you are not using a pre-baked image._

## Manager Setup Steps

Manager Setup is the last phase of execution. A file called `./instructions.txt` is created in your `cwd`. It documents follow-up steps to complete Manager configuration.

_If you choose the `bootstrap: true` option before execution, you will need to follow all of the steps documented in the `./instructions.txt` file._

_If you choose the `bootstrap: false` option before execution, you will only need to execute step 4._


These are the Manager setup steps:

0. Run this command to get the path to the instructions file:

```shell
$ cfy deployments outputs -b cloudify-environment-setup-latest/
```

The output should look similar to:

```json
{
  "1-Instructions": "/path/to/cwd/instructions.txt",
  "2-Demo": "cfy install https://github.com/cloudify-examples/nodecellar-auto-scale-auto-heal-blueprint/archive/4.1.zip -b demo -n aws-blueprint.yaml"
}
```

1. SSH into your Manager VM.

```shell
ssh -i ~/.ssh/cfy-manager-key-os centos@10.239.0.209
```

2. Install the Cloudify RPM on the Manager VM.

```shell
sudo rpm -i http://repository.cloudifysource.org/cloudify/4.1.0/ga-release/cloudify-enterprise-cli-4.1.rpm
```

3. Bootstrap the Manager:

```shell
cfy bootstrap /opt/cfy/cloudify-manager-blueprints/simple-manager-blueprint.yaml -i public_ip=10.239.0.209 -i private_ip=192.168.120.5 -i ssh_user=centos -i ssh_key_filename=/home/centos/.ssh/key.pem -i agents_user=ubuntu -i ignore_bootstrap_validations=false -i admin_username=admin -i admin_password=admin
```

4. Exit your Manager VM and initialize your CLI profile.

```shell
cfy profiles use -s centos -k ~/.ssh/cfy-manager-key-os -u admin -p admin -t default_tenant 10.239.0.209
```

5. Create Secrets.

```shell
cfy secrets create ......
```

6. Upload Plugins

```shell
cfy plugins upload ......
```


_Your manager is now ready. Proceed to the example blueprints!_

Try the [Nodecellar Auto-scale Auto-heal](https://github.com/cloudify-examples/nodecellar-auto-scale-auto-heal-blueprint/tree/4.1).


## Environment Teardown Steps

When you are ready to uninstall your environment, run:

```shell
$ cfy profiles use local
$ cfy uninstall --allow-custom-parameters -p ignore_failure=true --task-retries=30 --task-retry-interval=5 -b cloudify-environment-setup-latest

```

# Troubleshooting


## 502 Bad Gateway

- If `cfy profiles use ...` fails with this output, the service has started in error state. Try restarting the VM.

```shell
<head><title>502 Bad Gateway</title></head>
<body bgcolor="white">
<center><h1>502 Bad Gateway</h1></center>
<hr><center>nginx/1.8.0</center>
</body>
</html>
```


## [Errno 61] Connection refused

- If `cfy profiles use ...` fails with the following output, then the server is refusing your connection because of too many requests. Most likely this is an issue with your network. Expect this issue to come up a lot until your network service improves.

```shell
Attempting to connect...
HTTPConnectionPool(host='**.***.***.***', port=80): Max retries exceeded with url: /api/v3/provider/context (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x10d9d0590>: Failed to establish a new connection: [Errno 61] Connection refused',))
```


## Connection aborted, BadStatusLine

- If `cfy profiles use ...` fails with the following output, check the internet connection.

```shell
Attempting to connect...
Can't use manager 34.226.3.116. ('Connection aborted.', BadStatusLine("''",))
```


## InfluxDB wont start

- If `cfy bootstrap...` will not progress beyond influxdb, there is an issue with accessing the InfluxDB service on that port. This can be either an issue with a security group rule, or the IP may not be the primary interface.

```shell
2017-07-19 06:03:35.359  CFY <manager> [influxdb_yrqzak.create] Task started 'fabric_plugin.tasks.run_script'
[10.239.1.41] out: /tmp2017-07-19 06:03:36.959  LOG <manager> [influxdb_yrqzak.create] INFO: Installing InfluxDB...
2017-07-19 06:03:37.048  LOG <manager> [influxdb_yrqzak.create] INFO: Checking whether SELinux in enforced...
2017-07-19 06:03:37.425  LOG <manager> [influxdb_yrqzak.create] INFO: Downloading resource influxdb_NOTICE.txt to /opt/cloudify/influxdb/resources/influxdb_NOTICE.txt
2017-07-19 06:03:39.387  LOG <manager> [influxdb_yrqzak.create] INFO: Checking whether /opt/cloudify/influxdb/resources/influxdb-0.8.8-1.x86_64.rpm is already installed...
2017-07-19 06:03:39.923  LOG <manager> [influxdb_yrqzak.create] INFO: yum installing /opt/cloudify/influxdb/resources/influxdb-0.8.8-1.x86_64.rpm...
2017-07-19 06:03:41.116  LOG <manager> [influxdb_yrqzak.create] INFO: Deploying InfluxDB configuration...
2017-07-19 06:03:41.200  LOG <manager> [influxdb_yrqzak.create] INFO: Deploying blueprint resource components/influxdb/config/config.toml to /opt/influxdb/shared/config.toml
2017-07-19 06:03:42.565  LOG <manager> [influxdb_yrqzak.create] INFO: Deploying blueprint resource components/influxdb/config/cloudify-influxdb to /etc/sysconfig/cloudify-influxdb
2017-07-19 06:03:43.561  LOG <manager> [influxdb_yrqzak.create] INFO: Deploying blueprint resource components/influxdb/config/cloudify-influxdb.service to /usr/lib/systemd/system/cloudify-influxdb.service
2017-07-19 06:03:45.063  LOG <manager> [influxdb_yrqzak.create] INFO: Deploying blueprint resource components/influxdb/config/logrotate to /etc/logrotate.d/influxdb
2017-07-19 06:03:46.568  LOG <manager> [influxdb_yrqzak.create] INFO: Waiting for 192.168.121.5:8086 to become available...
2017-07-19 06:05:53.842  LOG <manager> [influxdb_yrqzak.create] INFO: 192.168.121.5:8086 is not available yet, retrying... (1/24)
[10.239.1.41] out:
[10.239.1.41] out:
[10.239.1.41] out:
```


## Invalid Block Device Mapping

- If `cfy install...` results in the below error, update the cloudify_host_block_device_mapping section to '/dev/sda1' in your input file.

```shell
<Response><Errors><Error><Code>InvalidBlockDeviceMapping</Code><Message>Invalid device name /dev/sda</Message></Error></Errors><RequestID>c1419ad6-5a27-457d-a8b7-d70c40ac8093</RequestID></Response>
```


## Instance type Availability Zone Mismatch

- If `cfy install ... aws-blueprint.yaml` execution fails with this error code, AWS is currently restricting deployments in your availability zone. Trying changing the availability zone to one of those suggested in the error message.


```
<Response><Errors><Error><Code>Unsupported</Code><Message>Your requested instance type (t1.micro) is not supported in your requested Availability Zone (us-east-1e). Please retry your request by not specifying an Availability Zone or choosing us-east-1a, us-east-1b, us-east-1d, us-east-1c.</Message></Error></Errors><RequestID>c00ced89-5e1d-4bcc-aac1-a8eff6e19935</RequestID></Response>
```
