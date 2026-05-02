#!/bin/bash
echo "Deleting cluster..."
gcloud container clusters delete sovereign-genesis --zone us-central1-a --project cogctl-gke-v01 --quiet

echo "Deleting NAT and Router..."
gcloud compute routers nats delete sovereign-nat --router=sovereign-router --region=us-central1 --project=cogctl-gke-v01 --quiet || true
gcloud compute routers delete sovereign-router --region=us-central1 --project=cogctl-gke-v01 --quiet || true

echo "Deleting Firewalls..."
FIREWALLS=$(gcloud compute firewall-rules list --project cogctl-gke-v01 --filter="name~'sovereign-'" --format="value(name)")
if [ ! -z "$FIREWALLS" ]; then
  for FW in $FIREWALLS; do 
    gcloud compute firewall-rules delete $FW --quiet --project cogctl-gke-v01
  done
fi

echo "Deleting Subnet and VPC..."
gcloud compute networks subnets delete sovereign-subnet --region=us-central1 --project=cogctl-gke-v01 --quiet || true
gcloud compute networks delete sovereign-vpc --project=cogctl-gke-v01 --quiet || true
echo "Purge complete."
