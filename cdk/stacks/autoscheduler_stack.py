from aws_cdk import Stack, aws_lambda as _lambda, aws_events as events, aws_events_targets as targets, Duration
from constructs import Construct
from cdk.utils.config import Config 
from cdk.utils.tags import apply_tags

class AutoSchedulerStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        config = Config(self)

        # Lambda Layers #######################################################

        self.powertools_layer_python = self.create_layer(
            scope,
            "PowertoolsLayer-python",
            f"arn:aws:lambda:{config.region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:79",
        )

        self.requests_toolbelt_layer = self.create_layer(
            scope, "RequestsToolbeltLayer", "lambda_layer/requests_toolbelt/layer.zip"
        )

        # Define the Lambda function with a prefixed name
        lambda_github_commit = _lambda.Function(
            self, config.prefixed_name("github-commit"),
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="github_commit.handler",
            code=_lambda.Code.from_asset("lambda/github_commit"),
            timeout=Duration.seconds(30),
        )

        # Add tags to the Lambda function
        for key, value in config.tags().items():
            Stack.of(self).tags.set_tag(key, value)

        # Define EventBridge rule
        rule = events.Rule(
            self, config.prefixed_name("DailyTrigger"),
            schedule=events.Schedule.expression("cron(0 10 * * ? *)")
        )

        # Attach Lambda as event target
        rule.add_target(targets.LambdaFunction(lambda_github_commit))