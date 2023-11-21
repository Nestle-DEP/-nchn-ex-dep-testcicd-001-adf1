#Requires -Version 3.0
#Requires -Module Az.Resources
#Requires -Module Az.Storage

Param(
    [string] $ResourceGroupName,
    [string] $TemplateFile,
    [string] $TemplateParametersFile,
    [string] $Mode = "Incremental",
    [string] $DeploymentName
)



New-AzResourceGroupDeployment -Name DeployLinkedTemplate -ResourceGroupName $ResourceGroupName -TemplateFile $TemplateFile -TemplateParameterFile $TemplateParametersFile -verbose
