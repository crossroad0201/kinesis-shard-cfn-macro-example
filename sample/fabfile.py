# -*- coding: utf-8 -*-
from __future__ import print_function
from fabric.api import *
from fabricawscfn import *
import boto3

env.AccountID = boto3.client('sts').get_caller_identity()['Account']

StackGroup('kinesis-shard-cfn-macro-sample-%(AccountID)s', 'templates', 'templates') \
    .define_stack('kinesis', 'kinesis-shard-cfn-macro-sample-kinesis', 'kinesis.yaml') \
    .define_stack('dashboard', 'kinesis-shard-cfn-macro-sample-dashboard', 'dashboard.yaml', Capabilities=['CAPABILITY_AUTO_EXPAND']) \
    .generate_task(globals())
