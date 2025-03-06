#!/usr/bin/env python3
import os
import boto3
import argparse
from dotenv import load_dotenv
import aws_cdk as cdk

from nntin_aws_cloudkit.nntin_aws_cloudkit_stack import NntinAwsCloudkitStack
from cdk.stacks.autoscheduler_stack import AutoSchedulerStack

def resolve_environment():
    """Resolve AWS account and region dynamically."""
    # Attempt to fetch the account ID and region from environment variables
    account = os.getenv("CDK_DEFAULT_ACCOUNT")
    region = os.getenv("CDK_DEFAULT_REGION")

    # If not set, use boto3 to fetch from the AWS CLI configuration
    if not account or not region:
        session = boto3.Session()
        account = account or session.client("sts").get_caller_identity()["Account"]
        region = region or session.region_name

    if not account or not region:
        raise EnvironmentError("Unable to resolve AWS account and region.")

    return cdk.Environment(account=account, region=region)

# Parse command-line arguments for environment selection
parser = argparse.ArgumentParser(
    description="Deploy CDK stack for a specific environment."
)
parser.add_argument(
    "--env",
    default=os.getenv("ENV", "dev"),
    help="The environment to deploy (e.g., dev, test, prod). Defaults to 'dev'.",
)
args = parser.parse_args()

# Dynamically load the corresponding .env file
env_file = f".env.{args.env}"
if not os.path.exists(env_file):
    raise FileNotFoundError(
        f"{env_file} not found. Please create the file or specify the correct environment."
    )
print(f"Loading environment variables from: {env_file}")
load_dotenv(env_file)

# Resolve environment
env = resolve_environment()

app = cdk.App()
AutoSchedulerStack(app, f"AutoSchedulerStack-{args.env}", env=env)

app.synth()