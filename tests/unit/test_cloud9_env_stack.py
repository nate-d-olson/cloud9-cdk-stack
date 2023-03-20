import aws_cdk as core
import aws_cdk.assertions as assertions

from cloud9_env.cloud9_env_stack import Cloud9EnvStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cloud9_env/cloud9_env_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Cloud9EnvStack(app, "cloud9-env")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
