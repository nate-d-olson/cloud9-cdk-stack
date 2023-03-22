#!/usr/bin/env python3
import os
from venv import EnvBuilder
from aws_cdk import (
    App,
    Aws,
    Environment,
    Tags,
    Duration,
    Stack
)

import aws_cdk as cdk
from cloud9_env.cloud9_env_stack import Cloud9EnvStack

ctk = {
    '@aws-cdk/core:permissionsBoundary': {
      'name': 'developer-policy'
    }}

app = cdk.App(context = ctk)
perm = app.node.try_get_context("@aws-cdk/core:permissionsBoundary")
print(perm)

cdk_env = cdk.Environment(account="752334989853", region="us-east-1")

Cloud9EnvStack(app, "Cloud9EnvStackTest", env = cdk_env)

app.synth()
