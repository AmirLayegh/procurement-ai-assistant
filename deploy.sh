# gcloud run deploy procurement-api \
#     --image us-central1-docker.pkg.dev/hackathon-461711/cloud-run-source-deploy/procurement-api:latest \
#     --region europe-north2 \
#     --allow-unauthenticated \
#     --port 8080 \
#     --memory 8Gi \
#     --cpu 4 \
#     --set-env-vars="ENVIRONMENT=production"


gcloud run deploy procurement-api \
    --source . \
    --region europe-north2 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 8Gi \
    --cpu 4 \
    --env-vars-file env.yaml


gcloud run deploy procurement-api \
  --source . \
  --platform managed \
  --region europe-north2 \
  --allow-unauthenticated \
  --memory 8Gi \
  --cpu 4