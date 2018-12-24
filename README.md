AWS CloudFormation macro example for Kinesis shard level metrics. 
====

## Requirements

* node.js
* Python 2.x

## Demo

### Deploy CloudFormation macro.

```
# Prepare deploy.
$ cd macro
$ rpm install -g serverless

# Deploy macro.
$ sls deploy -V
```

### Create Kinesis stream and dashboard.

```
# Prepare sample.
$ cd sample
$ pip install -r requirements.txt

# Create S3 bucket for CloudFormation template, and upload templates.
$ aws s3api create-bucket --bucket kinesis-shard-cfn-macro-sample-YOUR_AWS_ACCOUNT_ID
$ fab sync_templates

# Create Kineis data stream. 
$ fab create_kinesis
ShardCount? 2

# Enable Kinesis shard level monitoring.
$ aws kinesis enable-enhanced-monitoring --stream-name kinesis-shard-cfn-macro-sample --shard-level-metrics IncomingRecords

# Create CloudWatch dashboard.
$ fab create_dashboard
```

### Update shard count and dashboard.

```
$ cd sample

# Update Kinesis shad count.
$ fab update_kinesis
ShardCount? [2] 4

# Update CloudWatch dashboard.
$ fab update_dashboard 
```
