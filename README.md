# 🚀 nntin-aws-cloudkit

**nntin-aws-cloudkit** is a collection of **AWS CDK examples** showcasing best practices for cloud automation, infrastructure as code (IaC), and serverless deployments.

![AWS CDK](https://img.shields.io/badge/AWS-CDK-blue?logo=amazon-aws&style=flat)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&style=flat)
![License](https://img.shields.io/github/license/tedlano/nntin-aws-cloudkit)

## 📌 Overview

This repository provides **modular AWS CDK templates** that demonstrate real-world automation patterns, serverless solutions, and cloud-native workflows. 

Current examples include:

- **Scheduled Lambda Execution** → Automate daily commits to GitHub via AWS Lambda & EventBridge


---

## 🔧 Project Structure

```sh
nntin-aws-cloudkit/
│── cdk/                     # AWS CDK infrastructure
│   ├── stacks/              # CDK stacks for different services
│   │   ├── autoscheduler_stack.py  # Example stack for scheduled Lambda
│   ├── utils/               # Helper modules (config, tagging, etc.)
│   ├── cdk_app.py           # Main CDK application entry point
│── lambda/                  # AWS Lambda function source code
│   ├── github_commit/       # Lambda function to commit to GitHub daily
│── scripts/                 # Utility scripts for setup and deployment
│── .env                     # Environment variables (ignored in Git)
│── README.md                # Project documentation
│── requirements.txt          # Python dependencies
│── .gitignore                # Ignore unnecessary files
```