from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    Duration,
    CfnOutput,
)
from constructs import Construct
from cdk.utils.config import Config
from cdk.utils.tags import apply_tags


def convert_to_PascalCase(snake_str):
    return "".join(
        word.capitalize()
        for word in snake_str.replace("-", " ").replace("_", " ").split()
    )


class AutoSchedulerStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.config = Config(self)
        apply_tags(self, self.config.tags())

        # Lambda Layers #######################################################

        self.powertools_layer_python = self.create_layer(
            self,
            "PowertoolsLayer-python",
            f"arn:aws:lambda:{self.config.region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:79",
        )

        self.requests_toolbelt_layer = self.create_layer(
            self, "RequestsToolbeltLayer", "lambda_layer/requests_toolbelt/layer.zip"
        )

        def create_lambda_function(
            self,
            resource_label,
            environment,
            layers=None,
            handler=None,
            runtime=_lambda.Runtime.PYTHON_3_11,
            timeout=60,
            retry_attempts=2,
            dead_letter_queue=None,
        ):

            handler = handler or f"{resource_label}.handler"

            default_environment = {
                "LOG_LEVEL": self.config.log_level,
                "POWERTOOLS_SERVICE_NAME": resource_label,
            }
            merged_environment = {**default_environment, **environment}
            ResourceLabel = convert_to_PascalCase(resource_label)

            lambda_resource = _lambda.Function(
                self,
                f"{ResourceLabel}Function",
                function_name=f"{self.config.prefix}-{resource_label}",
                runtime=runtime,
                handler=handler,
                code=_lambda.Code.from_asset(f"lambda/{resource_label}"),
                layers=layers,
                environment=merged_environment,
                timeout=Duration.seconds(timeout),
                retry_attempts=retry_attempts,
                dead_letter_queue=dead_letter_queue,
            )

            CfnOutput(
                self,
                f"{ResourceLabel}FunctionName",
                value=lambda_resource.function_name,
            )
            CfnOutput(
                self,
                f"{ResourceLabel}FunctionArn",
                value=lambda_resource.function_arn,
            )

            return lambda_resource

        # Define the Lambda function with a prefixed name
        self.lambda_github_commit = create_lambda_function(
            self,
            resource_label="github_commit",
            environment={
                "GITHUB_TOKEN": self.config.github_token,
                "GITHUB_USERNAME": self.config.github_username,
                "GITHUB_REPO": self.config.github_repo,
            },
            layers=[self.powertools_layer_python, self.requests_toolbelt_layer],
            timeout=10,
        )

        # Define EventBridge rule
        self.rule = events.Rule(
            self,
            self.config.prefixed_name("DailyTrigger"),
            schedule=events.Schedule.expression("cron(0 10 * * ? *)"),
        )

        # Attach Lambda as event target
        self.rule.add_target(targets.LambdaFunction(self.lambda_github_commit))

    @staticmethod
    def create_layer(
        scope: Construct,
        layer_name: str,
        code_or_arn: str,
        compatible_runtimes: list = [_lambda.Runtime.PYTHON_3_11],
        description: str = None,
    ) -> _lambda.LayerVersion:
        """
        Creates an AWS Lambda Layer from a local asset or ARN.
        """
        if code_or_arn.startswith("arn:"):
            return _lambda.LayerVersion.from_layer_version_arn(
                scope, layer_name, code_or_arn
            )
        else:
            return _lambda.LayerVersion(
                scope,
                layer_name,
                code=_lambda.Code.from_asset(code_or_arn),
                compatible_runtimes=compatible_runtimes,
                description=description,
            )
