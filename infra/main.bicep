param namePrefix string = 'foundry-dev'
param uniqueSuffix string = uniqueString(resourceGroup().id)
param aiFoundryName string = '${namePrefix}-fd-${uniqueSuffix}'
param aiProjectName string = '${namePrefix}-proj-${uniqueSuffix}'
param location string = 'eastus'

/*
  An AI Foundry resources is a variant of a CognitiveServices/account resource type
*/ 
resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-09-01' = {
  name: aiFoundryName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  properties: {
    // required to work in AI Foundry
    allowProjectManagement: true

    // Defines developer API endpoint subdomain
    customSubDomainName: aiFoundryName

    disableLocalAuth: false
  }
}

// Deploy AI Project using module
module aiProjectModule './modules/project.bicep' = {
  name: 'aiProjectDeployment'
  params: {
    projectName: aiProjectName
    location: location
    resourceName: aiFoundry.name
  }
}

// Deploy Search service using module
module searchServiceModule './modules/search.bicep' = {
  name: 'searchServiceDeployment'
  params: {
    resourceName: aiFoundry.name
    searchName: '${namePrefix}-search-${uniqueSuffix}'
    location: location
  }
}

// Deploy Model using module
module modelDeploymentModule './modules/model-deployment.bicep' = {
  name: 'modelDeploymentDeployment'
  params: {
    resourceName: aiFoundry.name
    deploymentName: 'gpt-5-nano-dev'
    modelName: 'gpt-5-nano'
    modelVersion: '2025-08-07'
  }
}

output foundryId string = aiFoundry.id
output foundryName string = aiFoundry.name
output foundryEndpoint string = aiFoundry.properties.endpoint
output foundryIdentityPrincipalId string = aiFoundry.identity.principalId
output projectId string = aiProjectModule.outputs.projectId
output deploymentName string = modelDeploymentModule.outputs.deploymentName
output searchName string = searchServiceModule.outputs.searchName
output searchEndpoint string = searchServiceModule.outputs.searchEndpoint
