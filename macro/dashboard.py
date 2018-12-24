import json
import boto3


def lambda_handler(event, context):
    print('Macro input = %s' % json.dumps(event, indent = 2))

    dashboard_name = event['params']['DashboardName']
    stream_name = event['params']['StreamName']

    print('Getting shards for stream %s...' % stream_name)
    shards = __get_shards(stream_name)
    print('Shard(s) = %s' % shards)

    macro_result = {
        "requestId": event['requestId'],
        "status": "success",
        "fragment": __generate_fragment(
            event,
            dashboard_name,
            stream_name,
            shards
        )
    }

    print('Macro result = %s' % macro_result)
    return macro_result


def __get_shards(stream_name):
    def is_open(shard):
        return 'EndingSequenceNumber' not in shard['SequenceNumberRange']

    list_shards_result = boto3.client('kinesis').list_shards(
        StreamName = stream_name
    )
    return [(shard['ShardId'], is_open(shard)) for shard in list_shards_result['Shards']]


def __generate_fragment(event, dashboard_name, stream_name, shards):
    dashboard_body = {
        "widgets": [
            {
                "type": "metric",
                "width": 24,
                "height": 9,
                "properties": {
                    "title": "%s IncomingRecords per shard" % stream_name,
                    "region": event['region'],
                    "view": "timeSeries",
                    "stacked": False,
                    "metrics": [__incoming_records(stream_name, shard[0], shard[1]) for shard in shards]
                }
            }
        ]
    }

    return {
        "Type": "AWS::CloudWatch::Dashboard",
        "Properties": {
            "DashboardName": dashboard_name,
            "DashboardBody": json.dumps(dashboard_body)
        }
    }


def __incoming_records(stream_name, shard_id, is_open):
    return [
        "AWS/Kinesis",
        "IncomingRecords",
        "ShardId", shard_id,
        "StreamName", stream_name,
        {
            "stat": "Sum",
            "label": shard_id if is_open else '%s(CLOSED)' % shard_id
        }
    ]
