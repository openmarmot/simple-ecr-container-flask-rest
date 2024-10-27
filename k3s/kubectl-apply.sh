#!/bin/bash

# Deploy to kubernetes from ECR
# andrew@openmarmot.com
# last update : Oct 2024
# note - if the image pull is failing, make sure the secret was created in this namespace


#set -e

# -- variables --
aws_account="$(aws sts get-caller-identity --query Account --output text)"
aws_region="us-west-2"
namespace_name="messageboard"
container_name="messageboard"
kubernetes_name="messageboard"
image_pull_secret_name="us-west-2-ecr-registry"
read -p "Enter the container tag: " container_tag

# we do this here because the secret has to exist prior to the deployment
# after this make sure your cron that creates the secret also has the second line here
kubectl create namespace ${namespace_name}
kubectl get secret ${image_pull_secret_name} --namespace=default -oyaml | grep -v '^\s*namespace:\s' | kubectl apply --namespace=${namespace_name} -f -

# this is so env variables in the yaml get evaluated
eval "cat <<EOF
$(<./deploy.yaml)
EOF
" | kubectl apply -f -

echo  "kubectl get services --namespace ${namespace_name}"
kubectl get services --namespace ${namespace_name}
echo "kubectl get pods --namespace ${namespace_name}"
kubectl get pods --namespace ${namespace_name}