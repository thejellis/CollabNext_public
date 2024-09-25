# Change these values to the ones used to create the App Service.
SUBSCRIPTION=0bdb7994-618e-43ab-9dc4-e5510263d104
RESOURCE_GROUP_NAME='collabnext_alpha'
APP_SERVICE_NAME='collabnext'

az login
az webapp up --runtime PYTHON:3.9 --sku B1 --logs

az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $APP_SERVICE_NAME \
    --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true

cd frontend
npm install --legacy-peer-deps
npm install @memgraph/orb
copy build ../backend

zip -r collab.zip backend -x '.??*'

az webapp deploy \
    --name $APP_SERVICE_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --src-path collab.zip