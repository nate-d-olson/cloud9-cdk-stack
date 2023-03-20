# © 2022 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
# This AWS Content is provided subject to the terms of the AWS Customer Agreement
# available at http://aws.amazon.com/agreement or other written agreement between
# Customer and either Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.


from dataclasses import dataclass
from typing import (
    Any,
    Dict,
)
import os
import aws_cdk as cdk
from aws_cdk import (
    Aws,
    Duration,
    Stack,
    aws_cloud9 as cloud9,
    aws_iam as iam
)
from constructs import Construct
# from cdk_use_cases.custom_cloud9_ssm import CustomCloud9Ssm

class Cloud9EnvStack(Stack):
    '''
    Cloudformation stack deploys a test lambda
    '''

    def __init__(
        self, scope: Construct, construct_id: str, **kwargs
    ) -> None:
        
        super().__init__(scope,construct_id,**kwargs)

        ##IAM Roles##
        # assmue_role_perm = iam.PolicyStatement()
        # assmue_role_perm.add_actions("sts:AssumeRole")
        # assmue_role_perm.add_resources("*")
        # instance_role = iam.Role(
        #     self, 'cloud9_role',
        #     assumed_by=iam.ServicePrincipal("cloud9.amazonaws.com")
        # )
        #arn:aws:iam::752334989853:role/aws-service-role/cloud9.amazonaws.com/AWSServiceRoleForAWSCloud9
        # iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSServiceRoleforAWSCloud9")
        # iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSCloud9SSMAccessRole")
        # # instance_role.add_to_policy(assmue_role_perm)

        # ## Ins
        # cfn_instance_profile = iam.CfnInstanceProfile(self, "AWSCloud9SSMInstanceProfile",
        #                                               roles=["AWSServiceRoleForAWSCloud9", "AWSCloud9SSMAccessRole"],
        #                                             #   instance_profile_name=instance_role.role_name
        #     )
        # ## Cloud9 Instance
        cfn_environment_eC2 = cloud9.CfnEnvironmentEC2(self, "MyCfnEnvironmentEC2",
            instance_type="t2.micro",

            # the properties below are optional
            automatic_stop_time_minutes=123,
            connection_type="CONNECT_SSH",
            description="cloud9-cdk-test",
            image_id="amazonlinux-2-x86_64",
            name="test",
            subnet_id="subnet-041b548dc227975b3",
        )

        # cfn_environment_eC2.add_depends_on(cfn_instance_profile)
