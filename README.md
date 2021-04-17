# Using Python on Google Cloud with Cloud Run

This sample is a simple Cloud Run service written in Python.
It converts Euros to USD.

Build and deploy this service by running the following commands:

```
$ gcloud builds submit --tag gcr.io/PROJECT_ID/euro-to-usd

$ gcloud run deploy --image gcr.io/PROJECT_ID/euro-to-usd
--platform managed
```

If you don't want to deploy a new Cloud Run service, install the Cloud Code plugin ([VS Code](https://marketplace.visualstudio.com/items?itemName=GoogleCloudTools.cloudcode&ssr=false#overview) | [JetBrains](https://plugins.jetbrains.com/plugin/8079-cloud-code)) and run it in a Cloud Run emulator ([VS Code](https://cloud.google.com/code/docs/vscode/developing-a-cloud-run-app) | [JetBrains](https://cloud.google.com/code/docs/intellij/developing-a-cloud-run-app)).


For more info, check out this sample's accompanying [Serverless Expeditions video](https://www.youtube.com/watch?v=s2TIWIzCftM).

# architecture
1. repo - github/mikceyperlstein/eur-to-usd.git
1. cloud build - runs and tags the dockerfile and pushes to artifactory
1. cloud run - runs the dockerfile

## Schedule : uses cloud scheduler
  - send to pub/sub topic `refresh-by-cron-1`

service on app listens to the refresh signal

