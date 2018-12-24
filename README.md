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

* See the created dashboard `kinesis-shard-cfn-macro-sample`.
The metrics for 2 shards(shardId-000000000000 and shardId-000000000001) should be displayed.

* And Lambda function of the macro is output following logs.
```
START RequestId: d03d3c71-0746-11e9-9d4e-17d174a4cad3 Version: $LATEST
Macro input = {
  "region": "us-east-1",
  "accountId": "************",
  "fragment": {},
  "transformId": "************::KinesisShardLevelDashboard",
  "params": {
    "DashboardName": "kinesis-shard-cfn-macro-sample",
    "StreamName": "kinesis-shard-cfn-macro-sample"
  },
  "requestId": "5dee2557-92ff-4223-8786-92cf1f04966d",
  "templateParameterValues": {}
}
Getting shards for stream kinesis-shard-cfn-macro-sample...
Shard(s) = [('shardId-000000000000', False), ('shardId-000000000001', False), ('shardId-000000000002', True), ('shardId-000000000003', True), ('shardId-000000000004', True), ('shardId-000000000005', True)]
Macro result = {'requestId': '5dee2557-92ff-4223-8786-92cf1f04966d', 'status': 'success', 'fragment': {'Type': 'AWS::CloudWatch::Dashboard', 'Properties': {'DashboardName': 'kinesis-shard-cfn-macro-sample', 'DashboardBody': '{"widgets": [{"type": "metric", "width": 24, "height": 9, "properties": {"title": "kinesis-shard-cfn-macro-sample IncomingRecords per shard", "region": "us-east-1", "view": "timeSeries", "stacked": false, "metrics": [["AWS/Kinesis", "IncomingRecords", "ShardId", "shardId-000000000000", "StreamName", "kinesis-shard-cfn-macro-sample", {"stat": "Sum", "label": "shardId-000000000000(CLOSED)"}], ["AWS/Kinesis", "IncomingRecords", "ShardId", "shardId-000000000001", "StreamName", "kinesis-shard-cfn-macro-sample", {"stat": "Sum", "label": "shardId-000000000001(CLOSED)"}], ["AWS/Kinesis", "IncomingRecords", "ShardId", "shardId-000000000002", "StreamName", "kinesis-shard-cfn-macro-sample", {"stat": "Sum", "label": "shardId-000000000002"}], ["AWS/Kinesis", "IncomingRecords", "ShardId", "shardId-000000000003", "StreamName", "kinesis-shard-cfn-macro-sample", {"stat": "Sum", "label": "shardId-000000000003"}], ["AWS/Kinesis", "IncomingRecords", "ShardId", "shardId-000000000004", "StreamName", "kinesis-shard-cfn-macro-sample", {"stat": "Sum", "label": "shardId-000000000004"}], ["AWS/Kinesis", "IncomingRecords", "ShardId", "shardId-000000000005", "StreamName", "kinesis-shard-cfn-macro-sample", {"stat": "Sum", "label": "shardId-000000000005"}]]}}]}'}}}
END RequestId: d03d3c71-0746-11e9-9d4e-17d174a4cad3
REPORT RequestId: d03d3c71-0746-11e9-9d4e-17d174a4cad3	Duration: 57.35 ms	Billed Duration: 100 ms 	Memory Size: 1024 MB	Max Memory Used: 32 MB
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

* See the dashboard again.
The metrics for 6 shards(shardId-000000000002 to shardId-000000000005) should be displayed.
shardId-000000000000 and shardId-000000000001 are mark as CLOSED.
