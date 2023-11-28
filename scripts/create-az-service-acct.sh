# Run this in the Azure Cloud Shell to create an app service account with limited scope.
# this service account is used by github actions to deploy the app to Azure.

#!/bin/bash

# Parameters
SERVICE_PRINCIPAL_NAME="AI_IC_LLM_Demos-1-Deployment-SP"
ROLE="Contributor" 
SUBSCRIPTION_ID="xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
RESOURCE_GROUP_NAME="AI_IC_LLM_Demos-1"

# Azure Login (Uncomment if on local machine)
# az login

# Create Service Principal with limited scope
SERVICE_PRINCIPAL=$(az ad sp create-for-rbac --name $SERVICE_PRINCIPAL_NAME --role $ROLE --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP_NAME)

# Output the result
echo "Service Principal Created:"
echo $SERVICE_PRINCIPAL


# Result will look like this:
# { 
#     "appId": "xxxx", 
#     "displayName": "xxxx", 
#     "password": "xxxx", 
#     "tenant": "xxxx"
# }

# In Github Secrets, you must set:
# AZURE_CLIENT_ID = appId.
# AZURE_CLIENT_SECRET = password.
# AZURE_TENANT_ID = tenant.

# Make sure to use quotes around the values in Github Secrets.
