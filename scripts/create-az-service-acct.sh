# Run this in the Azure Cloud Shell to create an app service account with limited scope.
# this service account is used by github actions to deploy the app to Azure.

#!/bin/bash

# Parameters
SERVICE_PRINCIPAL_NAME="AI_IC_LLM_Demos-1-Deployment-SP"
ROLE="Contributor" 
SUBSCRIPTION_ID="dda1b514-139b-4eb2-8191-20a31a14d873"
RESOURCE_GROUP_NAME="AI_IC_LLM_Demos-1"

# Azure Login (Uncomment if on local machine)
# az login


az ad sp create-for-rbac --name $SERVICE_PRINCIPAL_NAME \
                            --role $ROLE \
                            --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP_NAME \
                            --sdk-auth
                            


# Result will look like this:
{
  "clientId": "xxx",
  "clientSecret": "xxx",
  "subscriptionId": "xxx",
  "tenantId": "xxx",
  "activeDirectoryEndpointUrl": "xxx",
  "resourceManagerEndpointUrl": "xxx",
  "activeDirectoryGraphResourceId": "xxx",
  "sqlManagementEndpointUrl": "xxx",
  "galleryEndpointUrl": "xxx",
  "managementEndpointUrl": "xxx""
}

# In Github Secrets, you must set:
# AZURE_CREDENTIALS: The JSON output from the above command.