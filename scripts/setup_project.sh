#!/bin/bash

echo "🚀 Setting up nntin-aws-cloudkit project structure..."

# Create main directories
mkdir -p cdk/stacks cdk/constructs lambda scripts examples docs tests

# Create stack and construct subfolders
touch cdk/stacks/__init__.py cdk/constructs/__init__.py
touch cdk/cdk_app.py

# Create lambda function directories
mkdir -p lambda/nntin_autoscheduler lambda/s3_event_processor lambda/common

# Add placeholder files for Lambda functions
touch lambda/nntin_autoscheduler/handler.py
touch lambda/nntin_autoscheduler/.env
touch lambda/nntin_autoscheduler/requirements.txt
touch lambda/s3_event_processor/handler.py
touch lambda/common/helpers.py

# Add README placeholders
touch examples/README.md docs/README.md tests/README.md


# Add .gitignore
echo "venv/" >> .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore

echo "✅ Project structure successfully set up!"