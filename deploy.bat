@echo off
echo Deploying Sanjeevani to Google Cloud Run...

if "%GEMINI_API_KEY%"=="" (
    echo ERROR: GEMINI_API_KEY environment variable is not set.
    echo Please set it before running this script:
    echo set GEMINI_API_KEY=your_api_key
    exit /b 1
)

gcloud run deploy sanjeevani --source . --port 8080 --region asia-south1 --allow-unauthenticated --set-env-vars GEMINI_API_KEY="%GEMINI_API_KEY%"
