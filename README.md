
# Simple Infrastructure Blueprint

## pre-requisites

- Cloudify CLI (run ```pip install cloudify```)
- AWS Account


## instructions

1. Create inputs file. When you cat the file it should look like this:

```shell
$ cat inputs.yaml
aws_secret_access_key: ....
aws_access_key_id: ....
```

_As an alternative to creating a file, you may append your credentials to the command in step 2 like this: ```-i aws_secret_access_key=... -i aws_access_key_id=...```_


2. Install the infrastructure:

```shell
$ cfy install aws-blueprint -i inputs.yaml --task-retries=30 --task-retry-interval=5
```


3. Show the outputs:

```shell
$ cfy deployments outputs
```


4. Follow the steps in the outputs.

_If ```cfy profiles use``` in Step1 returns a ```connection refused``` error, the manager is still getting started so wait a few moments and try again._
