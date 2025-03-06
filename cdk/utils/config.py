import os
from aws_cdk import Stack


class Config:
    def __init__(self, stack: Stack):
        self.env = os.getenv("ENV", "dev").strip()
        self.company = os.getenv("COMPANY", "nntin").strip()
        self.project = os.getenv("PROJECT", "aws-cloudkit").strip()
        self.owner = os.getenv("OWNER", "tlano").strip()
        self.log_level = os.getenv("LOG_LEVEL", "INFO").strip()

        self.region = stack.region
        self.account = stack.account
        self.prefix = f"{self.company}-{self.env}-{self.project}"

    def tags(self):
        return {
            "environment": self.env,
            "project": self.project,
            "owner": self.owner,
        }
    
    def prefixed_name(self, name: str):
        """Returns a standardized name for AWS resources using the prefix."""
        return f"{self.prefix}-{name}"
