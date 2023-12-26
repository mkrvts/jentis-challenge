
# City-Weather Microservice and Infrastructure Deployment

## Overview
This repository houses the source code for the city-weather microservice and Terraform code to deploy the associated infrastructure. The microservice provides real-time weather information in a selected city (defined in the code), and the infrastructure is orchestrated on Azure using Terraform.

## Prerequisites
Before deploying the application and infrastructure, ensure the following prerequisites are met:
- Configured access to an Azure subscription via Azure CLI
- Installed Terraform
- Installed kubectl
- Installed Helm

## Deploying Infrastructure with Terraform
1. Create an Active Directory service principal account:
   ```sh
   az ad sp create-for-rbac --skip-assignment
   ```

2. Update the `terraform.tfvars` file with values from the previous command:
   ```hcl
   appId    = "<appId>"
   password = "<password>"
   ```

3. Apply Terraform configuration:
   ```sh
   terraform init
   terraform plan
   terraform apply
   ```

4. Retrieve access credentials for the newly created Kubernetes cluster:
   ```sh
   az aks get-credentials --resource-group $(terraform output -raw resource_group_name) --name $(terraform output -raw kubernetes_cluster_name)
   ```

## Monitoring
To install monitoring on your cluster, run the following commands:
```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install latest prometheus-community/kube-prometheus-stack
```

## Application Deployment
1. Build the image on Azure Container Registry:
   - Set environment variables:
     ```sh
     AZURE_CONTAINER_REGISTRY=jentischallengeacr
     CONTAINER_NAME=jentis-challenge-app
     RESOURCE_GROUP=jentis-challenge-rg
     CLUSTER_NAME=jentis-challenge-aks
     ```

   - Run `az build` from the `/app` directory:
     ```sh
     az acr build --image $AZURE_CONTAINER_REGISTRY.azurecr.io/$CONTAINER_NAME --registry $AZURE_CONTAINER_REGISTRY -g $RESOURCE_GROUP .
     ```

2. Deploy the application to the AKS cluster:
   ```sh
   cd app
   helm install city-weather-app ./helm --namespace application --create-namespace 
   ```

3. Verify that application pods are running:
   ```sh
   kubectl get pods -n application
   ```