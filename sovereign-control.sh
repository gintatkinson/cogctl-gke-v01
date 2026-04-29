#!/bin/bash

# Sovereign Genesis: Deterministic Control Script (The Gate)
# Usage: ./sovereign-control.sh [start|stop]

set -e

ACTION=$1

if [ -z "$ACTION" ]; then
  echo "Usage: ./sovereign-control.sh [start|stop]"
  exit 1
fi

check_terraform() {
  if ! command -v terraform &> /dev/null; then
    if [ ! -f "./terraform" ]; then
      echo "Terraform not found. Downloading standalone binary (aarch64)..."
      curl -Lo terraform.zip https://releases.hashicorp.com/terraform/1.8.2/terraform_1.8.2_linux_arm64.zip
      unzip -o terraform.zip
      rm terraform.zip
      chmod +x terraform
    fi
    export PATH="$PATH:$(pwd)"
  fi
}

check_vpc_preflight() {
  echo "Checking for VPC pollution..."
  VPC_TIMESTAMP=$(gcloud compute networks describe sovereign-vpc --format="value(creationTimestamp)" 2>/dev/null || echo "")
  if [ ! -z "$VPC_TIMESTAMP" ]; then
    echo "WARNING: sovereign-vpc already exists (Created: $VPC_TIMESTAMP)."
    echo "This violates the Zero-State baseline mandate. Aborting start."
    echo "Please execute ./sovereign-control.sh stop first to ensure a clean birth."
    exit 1
  fi
}

# Inject credentials for Terraform
export GOOGLE_OAUTH_ACCESS_TOKEN=$(gcloud auth print-access-token)

if [ "$ACTION" == "start" ]; then
  echo "==== [PHASE 0] Pre-flight Validation ===="
  check_vpc_preflight
  
  echo "==== [PHASE 1] Birthing Infrastructure (Terraform) ===="
  check_terraform
  cd infra/terraform
  ../../terraform init
  ../../terraform apply -auto-approve
  cd ../..

  echo "==== [PHASE 2] Biting Services (Certified Pipeline) ===="
  gcloud builds submit --config infra/cloudbuild_graduation_final.yaml \
    --substitutions=_TAG="rc13-verified",_CLUSTER_NAME="sovereign-genesis",_ZONE="us-central1-a" .

  echo "==== [STARTUP COMPLETE] ===="

elif [ "$ACTION" == "stop" ]; then
  echo "==== [PHASE 1] Destroying Infrastructure (Terraform) ===="
  check_terraform
  cd infra/terraform
  ../../terraform init
  ../../terraform destroy -auto-approve
  cd ../..
  
  echo "==== [SHUTDOWN COMPLETE] ===="

else
  echo "Unknown action: $ACTION. Use 'start' or 'stop'."
  exit 1
fi
