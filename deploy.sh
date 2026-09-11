#!/bin/bash
echo "Deploying Sanjeevani to Google Cloud Run..."

if [ -z "$GEMINI_API_KEY" ]; then
    echo "ERROR: GEMINI_API_KEY environment variable is not set."
    echo "Please set it before running this script:"
    echo "export GEMINI_API_KEY=your_api_key"
    exit 1
fi

gcloud run deploy sanjeevani --source . --port 8080 --region asia-south1 --allow-unauthenticated --set-env-vars GEMINI_API_KEY="$GEMINI_API_KEY"
