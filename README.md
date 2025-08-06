# simple-ecr-container-flask-rest
Simple Docker container hosting a flask webserver with a REST API 

This is a simple Flask website that can receive and display messages through a REST API
I needed this to test something else, so I threw it up here.

Note - CORS is optional but useful if you are trying to display the data on another website

### Setup
- create a AWS IAM user and attach the AmazonEC2ContainerRegistryFullAccess IAM policy
- click the user in IAM->Security Credentials -> create access key
- configure the aws cli on your machine (aws configure). enter the access key and set the region
- update build_and_push_to_ecr.sh with the container name and region you want
- create your private ECR repo in the AWS ECR console
- run build_and_push_to_ecr.sh to build the docker container and push it to ECR

### Kubernetes Deploy
- k3s/kubectl-apply.sh is a simple deployment aimed at a k3s host.
- It is designed to work with a K3s server deployed with this template [k3s with aws ecr](https://github.com/openmarmot/ansible-stuff/blob/main/fedora-k3s-with-aws-ecr.yml)