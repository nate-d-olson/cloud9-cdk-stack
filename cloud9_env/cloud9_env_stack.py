# © 2022 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
# This AWS Content is provided subject to the terms of the AWS Customer Agreement
# available at http://aws.amazon.com/agreement or other written agreement between
# Customer and either Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.

from aws_cdk import (
    Stack,
    aws_cloud9 as cloud9,
    aws_iam as iam
)
from constructs import Construct

class Cloud9EnvStack(Stack):
    '''
    Cloudformation stack deploys a Cloud9 environment
    '''
    ## Stack definition based on cloud9 documentation found here
    ##          https://docs.aws.amazon.com/cloud9/latest/user-guide/security-iam.html#auth-and-access-control-managed-policies
    ##          and code from chatGPT session

    def __init__(
        self, scope: Construct, construct_id: str, **kwargs
    ) -> None:
        
        super().__init__(scope,construct_id,**kwargs)

        # Create a Cloud9 environment
        c9_env = cloud9.CfnEnvironmentEC2(self, "MyCloud9Env",
                                          name="cc9-cdk-test",
                                          instance_type="t2.micro",
                                          subnet_id="subnet-041b548dc227975b3",
                                          automatic_stop_time_minutes=30)
        
        # Create an IAM role for the Cloud9 environment
        c9_role = iam.Role(self, "MyCloud9Role",
                           assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                           managed_policies=[
                               iam.ManagedPolicy.from_aws_managed_policy_name(
                                   "CloudWatchLogsFullAccess")
                           ],
                           permissions_boundary= iam.ManagedPolicy.from_aws_managed_policy_name("developer-policy"))
        
        # Add permissions to the IAM role
        c9_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ssm:StartSession"],
            resources=["*"]
        ))

        c9_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["sts:AssumeRole"],
            resources=["*"]
        ))

        print(c9_role.role_arn)
        # Attach the IAM role to the Cloud9 environment
        c9_env.add_property_override("OwnerArn", c9_role.role_arn)

        # Set the Cloud9 connection method
        c9_env.add_property_override("ConnectionType", "CONNECT_SSM")
