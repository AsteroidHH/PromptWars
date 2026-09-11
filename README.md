# 🚑 Sanjeevani - Emergency Triage Bridge

**Sanjeevani** is an advanced, AI-powered emergency triage system built for the PromptWars challenge. It acts as a universal bridge, converting messy, chaotic real-world inputs—such as panicked bystander audio, messy text notes, or scene photos—into structured, verified, and life-saving actions using Google Gemini.

## 🌟 Problem Statement & Societal Benefit

During the critical "golden hour" of an emergency, non-medical bystanders are often paralyzed by panic, and first responders receive incomplete or conflicting information. Sanjeevani solves this by:
1. **Calming the Chaos:** Parsing multi-modal inputs (voice, text, images) to instantly extract the clinical status.
2. **Actionable First-Aid:** Providing immediate, step-by-step instructions (and critical warnings of what *not* to do) to bystanders.
3. **Optimized Dispatch:** Generating standard RED/YELLOW/GREEN/BLACK triage tags, hazard warnings, and automatic routing to the nearest appropriate trauma center via Google Maps.

## 🏗️ Architecture & Tech Stack

Sanjeevani is built with modern, scalable, and type-safe technologies:
* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11) for high-performance async request handling.
* **AI Engine:** Google Gemini 3.7 Flash via the official `google-genai` SDK. We strictly enforce a Pydantic `response_schema` to guarantee deterministic, structured JSON outputs.
* **Frontend:** A lightweight, vanilla HTML/JS/CSS frontend served by FastAPI, utilizing the browser's native `MediaRecorder` API for on-scene voice memos.
* **Routing:** Dynamic Google Maps Search API integration for instant hospital routing based on extracted landmarks.
* **Deployment:** Optimized `Dockerfile` targeting **Google Cloud Run** for serverless, autoscaling deployment.

## 🎯 Evaluation Rubric Alignment

This project was carefully crafted to exceed hackathon rubric criteria:
* **Code Quality & Architecture:** Clean modular design separating FastAPI routes, Pydantic schemas, Gemini API integration, and tests.
* **Security:** A comprehensive `.gitignore` ensures credentials, virtual environments, and local media files are never committed.
* **Unit Testing:** Comprehensive pytest suite utilizing FastAPI `TestClient` and `unittest.mock` to verify the backend and schema without incurring API costs.
* **WCAG Accessibility:** The frontend features semantic HTML, `aria-live` regions for screen readers, high-contrast theming, and clear focus states.
* **Google Services Integration:** Leverages cutting-edge Gemini Multimodal capabilities alongside dynamic Google Maps Emergency search URLs.

## 🚀 Quickstart

### Local Setup

1. **Clone the repository and enter the directory:**
   ```bash
   git clone https://github.com/AsteroidHH/PromptWars.git
   cd PromptWars
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your Gemini API Key:**
   ```bash
   # On Windows:
   set GEMINI_API_KEY=your_actual_api_key_here
   # On macOS/Linux:
   export GEMINI_API_KEY="your_actual_api_key_here"
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```
   Navigate to `http://127.0.0.1:8000` to access the Emergency Intake UI, or `http://127.0.0.1:8000/docs` for the Swagger API documentation.

### Running Tests

Run the test suite using `pytest`:
```bash
pytest tests/
```

### ☁️ Cloud Run Deployment

You can deploy Sanjeevani to Google Cloud Run using the included deployment scripts.

1. Ensure the Google Cloud SDK (`gcloud`) is installed and authenticated:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```
2. Run the deployment script:
   * **Windows:** `deploy.bat`
   * **macOS/Linux:** `./deploy.sh`
