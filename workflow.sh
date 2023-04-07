az group create --name def_resource_group --location francecentral
az configure defaults --group=def_resource_group
az ml workflow create --name def-workflow
az configure defaults --workflow=def-workflow
# az data create --name diabetes-dev-folder --path /experimentation/data
# az compute create --name def-cluster --size STANDARD_DS11_V2 --max-instances 2 --type AmlCompute
# gh workflow run .github/workflows/02-manual-trigger-job.yml 