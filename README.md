Overview
========

A package to upload config ini files to [AWS Systems Manager Parameter Store](https://aws.amazon.com/ec2/systems-manager/parameter-store/)

```
$ aws-parameter-uploader --help
Usage: aws-parameter-uploader [OPTIONS] FILENAME

Options:
  --namespace TEXT  The application name
  --env TEXT        The application environment (pilot, prod, etc..)
  --help            Show this message and exit.
```


Purpose
=======

It will take a file in this format:
```
[database]
username = test
password = test

[redis]
host = redis.server.test
```

namespace = myapp
env = prod

and upload into AWS Systems Manager Parameter Store:


Installation
============
```
pip install aws-parameter-uploader
```

This project uses boto3. [It will require AWS credentials properly configured](http://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials).
