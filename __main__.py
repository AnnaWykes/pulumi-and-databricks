"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources
from pulumi_azure_native import databricks as dbx

# Create an Azure Resource Group
resource_group = resources.ResourceGroup('pulumi_databricks_resource_group')

# Create an Azure resource (Storage Account)
account = storage.StorageAccount('pulumidbxsa',
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(
        name=storage.SkuName.STANDARD_LRS,
    ),
    kind=storage.Kind.STORAGE_V2)

# Export the primary key of the Storage Account
primary_key = pulumi.Output.all(resource_group.name, account.name) \
    .apply(lambda args: storage.list_storage_account_keys(
        resource_group_name=args[0],
        account_name=args[1]
    )).apply(lambda accountKeys: accountKeys.keys[0].value)
    

workspace = dbx.Workspace("workspace",
    location="westus",
    managed_resource_group_id="/subscriptions/167ab168-84f9-43c4-b197-8bfbf27bf6d1/resourceGroups/pulumi_databricks_managed_resource_group",
    parameters=dbx.WorkspaceCustomParametersArgs(
        prepare_encryption=dbx.WorkspaceCustomBooleanParameterArgs(
            value=True,
        ),
    ),
    resource_group_name=resource_group.name,
    workspace_name="pulumi_databricks_workspace")

pulumi.export("primary_storage_key", primary_key)
