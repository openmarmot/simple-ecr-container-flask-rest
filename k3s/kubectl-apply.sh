#!/bin/bash

# Deploy to kubernetes from ECR
# andrew@openmarmot.com
# last update : Oct 2024

set -e

# -- variables --
#aws account number
aws_account="$(aws sts get-caller-identity --query Account --output text)"
aws_region="us-west-2"
container_name="messageboard"
kubernetes_name="messageboard"
read -p "Enter the container tag: " container_tag

# this is so env variables in the yaml get evaluated
eval "cat <<EOF
$(<./deploy.yaml)
EOF
" | kubectl apply -f -

echo '-- kubectl get services --'
kubectl get services | grep ${kubernetes_name}
echo '-- kubectl get pods --'
kubectl get pods | grep ${kubernetes_name}