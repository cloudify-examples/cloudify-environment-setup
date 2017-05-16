
# Cloudify Environment Blueprint

Provisions infrastructure and starts a Cloudify Manager.


### purpose

Cloudify Manager is designed to work in any environment, whether cloud, baremetal, or a hybrid of the two. This blueprint will deploy the reference environment that is used by other examples.


## pre-requisites

- [Cloudify CLI](http://docs.getcloudify.org/4.0.0/installation/from-packages/) installed on your computer.
- [AWS Account Credentials](http://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)


## instructions

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

If that is the case, restart the VM.


4. To uninstall the demo app, run:

```shell
$ cfy uninstall demo --allow-custom-parameters -p ignore_failure=true
```


5. To uninstall the example environment, run:

```shell
$ cfy profiles use local
$ cfy uninstall --allow-custom-parameters -p ignore_failure=true --task-retries=30 --task-retry-interval=5
```
