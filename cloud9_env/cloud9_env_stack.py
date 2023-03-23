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
    PermissionsBoundary,
    Stack,
    aws_cloud9 as cloud9,
    aws_iam as iam
)
from constructs import Construct
# from cdk_use_cases.custom_cloud9_ssm import CustomCloud9Ssm

class Cloud9EnvStack(Stack):
    '''
    Cloudformation stack deploys a Cloud9 environment
    '''
    ## Stack definition based on cloud9 documentation found here
    ##          https://docs.aws.amazon.com/cloud9/latest/user-guide/security-iam.html#auth-and-access-control-managed-policies
    ##          
    def __init__(
        self, scope: Construct, construct_id: str, **kwargs
    ) -> None:
        
        super().__init__(scope,construct_id,**kwargs)

        ##IAM Roles ###############################################################################################################

        ## Policy statements for Instance role
        ##      Policy Statements based off of https://docs.aws.amazon.com/cloud9/latest/user-guide/ec2-ssm.html#aws-cli-instance-profiles
        assume_role_perm = iam.PolicyStatement()
        assume_role_perm.add_actions("sts:AssumeRole")
        assume_role_perm.add_resources("*")

        ## Added based on "Actions supported by AWS managed temporary credentials" from https://docs.aws.amazon.com/cloud9/latest/user-guide/security-iam.html#auth-and-access-control-customer-policies
        ## -- hoping to get decoded ec2:RunInstances error message
        ## Including these actions cdk still runs but deployment fails with ec2:RunInstances error
        # assume_role_perm.add_actions("sts:GetCallerIdentity")
        # assume_role_perm.add_actions("sts:DecodeAuthorizationMessage")
        
        ## Added based on "AWS Cloud9 resources and operations" from https://docs.aws.amazon.com/cloud9/latest/user-guide/security-iam.html#auth-and-access-control-managed-policies
        c9resource_role_perm = iam.PolicyStatement()
        c9resource_role_perm.add_actions("cloud9:*")
        c9resource_role_perm.add_resources("arn:aws:cloud9:*")
        
        ssmec2_role_perm = iam.PolicyStatement()
        ssmec2_role_perm.add_actions("ssm:StartSession")
        ssmec2_role_perm.add_resources("arn:aws:ec2:*:*:instance/*")
        ssmec2_role_perm.add_condition("StringLike", {"ssm:resourceTag/aws:cloud9:environment": "*"})
        ssmec2_role_perm.add_condition("StringEquals", {"aws:CalledViaFirst": "cloud9.amazonaws.com"})

        ssmdoc_role_perm = iam.PolicyStatement()
        ssmdoc_role_perm.add_actions("ssm:StartSession")
        ssmdoc_role_perm.add_resources("arn:aws:ssm:*:*:document/*")

        ## Creating roles for instance with AWSCloud9 instance policy
        instance_role = iam.Role(
            self,
            "AWSCloud9SSMAccessRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("cloud9.amazonaws.com"),
                iam.ServicePrincipal("ec2.amazonaws.com")
            ),
            # permissions boundaries needed for deploying in NIST AWS account
            permissions_boundary = iam.ManagedPolicy.from_aws_managed_policy_name("developer-policy"),
            path="/service-role/"
        )

        instance_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSCloud9SSMInstanceProfile"))
        
        instance_role.add_to_policy(assume_role_perm)
        instance_role.add_to_policy(c9resource_role_perm)
        instance_role.add_to_policy(ssmec2_role_perm)
        instance_role.add_to_policy(ssmdoc_role_perm)

        ## Not sure where or if I need to add these policies
        # cloud9_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSCloud9Administrator"))
        # cloud9_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSCloud9User"))
        # cloud9_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSCloud9EnvironmentMember"))

        ## Ins
        cfn_instance_profile = iam.CfnInstanceProfile(self, "c9InstanceProfile",
                                                      roles=[instance_role.role_name],
                                                      instance_profile_name="AWSCloud9SSMInstanceProfile",
                                                      path="/cloud9/",
            )
        ## Not sure how to do this step from https://docs.aws.amazon.com/cloud9/latest/user-guide/ec2-ssm.html#aws-cli-instance-profiles
        #       "After defining a service role and instance profile in the AWS CloudFormation template, 
        #        ensure that the IAM entity creating the stack has permission to start a Session Manager session. "

        # print(cloud9_role.role_name)
        ## Cloud9 Instance ###############################################################################################################
        cfn_environment = cloud9.CfnEnvironmentEC2(self, "MyCfnEnvironmentEC2",
            instance_type="t2.micro",

            # the properties below are optional
            automatic_stop_time_minutes=123,
            connection_type="CONNECT_SSM",
            description="cloud9-cdk-test",
            # image_id="amazonlinux-2-x86_64",
            ## Is this where/ how to create the EC2 environment with appropriate roles 
            owner_arn=instance_role.role_arn,
            name="test",
            subnet_id="subnet-041b548dc227975b3",
        )

        ## ensuring instance role is created first
        cfn_environment.add_depends_on(cfn_instance_profile)
        # cfn_environment.add_depends_on(cloud9_role)

        ## Not sure if I need to do this step from https://docs.aws.amazon.com/cloud9/latest/user-guide/ec2-ssm.html#aws-cli-instance-profiles
        #   " Configuring VPC endpoints for Amazon S3 to download dependencies"
        ##  if so - need to figure out how
