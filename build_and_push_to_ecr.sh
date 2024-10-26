#!/bin/bash

# build docker image and push to AWS ECR
# andrew@openmarmot.com
# last update : Oct 2024
# note - create the ECR repo in the Amazon console before running

set -e

# -- variables --
#aws account number
aws_account="$(aws sts get-caller-identity --query Account --output text)"
aws_region="us-west-2"
container_name="messageboard"
container_tag=$(date +%b-%d-%Y-%k-%M)

# -- docker build/push --

cd docker

aws ecr get-login-password --region ${aws_region} | docker login --username AWS --password-stdin ${aws_account}.dkr.ecr.${aws_region}.amazonaws.com

docker build -t ${container_name} .

docker tag ${container_name}:latest ${aws_account}.dkr.ecr.${aws_region}.amazonaws.com/${container_name}:${container_tag}

docker push ${aws_account}.dkr.ecr.${aws_region}.amazonaws.com/${container_name}:${container_tag}