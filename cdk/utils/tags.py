from aws_cdk import Tags


def apply_tags(scope, tags: dict):
    for key, value in tags.items():
        Tags.of(scope).add(key, value)
