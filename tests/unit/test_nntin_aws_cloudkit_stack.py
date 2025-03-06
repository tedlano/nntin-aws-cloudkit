import aws_cdk as core
import aws_cdk.assertions as assertions

from nntin_aws_cloudkit.nntin_aws_cloudkit_stack import NntinAwsCloudkitStack


# example tests. To run these tests, uncomment this file along with the example
# resource in nntin_aws_cloudkit/nntin_aws_cloudkit_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = NntinAwsCloudkitStack(app, "nntin-aws-cloudkit")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
