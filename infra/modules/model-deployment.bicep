@description('Parent AI Foundry account name.')
param resourceName string

@description('Name of the model deployment.')
param deploymentName string

@description('Model name.')
param modelName string

@description('Model format.')
param modelFormat string = 'OpenAI'

@description('Model version.')
param modelVersion string

@description('SKU capacity.')
param skuCapacity int = 1

@description('SKU name.')
param skuName string = 'GlobalStandard'

resource aiFoundryAccount 'Microsoft.CognitiveServices/accounts@2025-09-01' existing = {
  name: resourceName
}

resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-09-01' = {
  parent: aiFoundryAccount
  name: deploymentName
  sku: {
    capacity: skuCapacity
    name: skuName
  }
  properties: {
    model: {
      name: modelName
      format: modelFormat
      version: modelVersion
    }
  }
}

output deploymentName string = modelDeployment.name
output deploymentId string = modelDeployment.id
