# Serverless Student Login Portal (AWS)

A serverless login application built on AWS.

## Architecture
Browser (Amplify) -> API Gateway -> Lambda (Python 3.12) -> DynamoDB

## Services used
- AWS Amplify: hosts index.html and dashboard.html
- Amazon API Gateway: REST API with POST /login and CORS enabled
- AWS Lambda: checks credentials (lambda_function.py)
- Amazon DynamoDB: `Students` table, partition key `username`
- AWS IAM: Lambda role with AmazonDynamoDBReadOnlyAccess (least privilege)

## How it works
1. The user enters a username and password on index.html.
2. The page sends a POST request to the API Gateway /login endpoint.
3. Lambda looks up the user in DynamoDB and compares the password.
4. On success, the user is redirected to dashboard.html.

## Possible improvements
- Hash passwords instead of storing plain text
- Use Amazon Cognito for authentication
- Restrict CORS to the site's own domain