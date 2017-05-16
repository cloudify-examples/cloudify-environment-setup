
# Cloudify Environment Blueprint

Provisions infrastructure and starts a Cloudify Manager.


## pre-requisites

- [Cloudify CLI](http://docs.getcloudify.org/4.0.0/installation/from-packages/) installed on your computer.
- [AWS Account Credentials](http://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)


## instructions

1. Download and extract this blueprint archive, [link](https://github.com/cloudify-examples/cloudify-environment-blueprint/archive/latest.zip), to your current working directory.


2. Install the infrastructure. This command must be run from the same directory in which you extracted the blueprint in the previous step.

```shell
$ cfy install cloudify-environment-blueprint-latest/aws-blueprint.yaml -i aws_secret_access_key=[INSERT_YOUR_AWS_SECRET_KEY] -i aws_access_key_id=[INSERT_YOUR_AWS_ACCESS_KEY] --task-retries=30 --task-retry-interval=5
```


3. Show the outputs:

```shell
$ cfy deployments outputs
```


4. Follow the steps in the outputs.

_If ```cfy profiles use``` in Step1 returns a ```connection refused``` error, the manager is still getting started so wait a few moments and try again._
