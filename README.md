HealthPay Claim Processor
A FastAPI-based backend for processing medical insurance claim documents using AI-driven agentic workflows with LangGraph orchestration. This project implements a /process-claim endpoint that accepts PDF uploads, classifies documents, extracts structured data, validates consistency, and returns a claim decision in a defined JSON schema, fulfilling the HealthPay Backend Developer Assignment.
Architecture

Framework: FastAPI with asynchronous endpoints for efficient file upload and processing.
Agent Orchestration: LangGraph orchestrates four agents:
ClassifierAgent (app/agents/classifier.py): Classifies PDFs as bill or discharge_summary using filename and extracted text, powered by Google Gemini (gemini-1.5-flash).
ExtractorAgent (app/agents/extractor.py): Extracts fields: hospital_name (string), total_amount (float), date_of_service (YYYY-MM-DD string) for bills; patient_name (string), diagnosis (string), admission_date (YYYY-MM-DD string), discharge_date (YYYY-MM-DD string) for discharge summaries.
ValidatorAgent (app/agents/validator.py): Checks for missing documents (requires both bill and discharge summary) and discrepancies (e.g., date mismatches).
DecisionAgent (app/agents/decision.py): Generates a claim decision (approved or rejected) with a reason.


LLM: Google Gemini (gemini-1.5-flash) handles classification, extraction, validation, and decision-making via structured JSON prompts.
File Processing: pdfplumber in app/utils/pdf_reader.py extracts text from PDFs, supporting multipart/form-data uploads.
Validation: Pydantic enforces JSON schema validation, with LLM-based cross-checks for logical consistency.
Workflow:
The /process-claim endpoint (app/main.py) accepts multiple PDFs via multipart/form-data.
Text is extracted using pdfplumber in pdf_reader.py.
ClassifierAgent identifies the document type.
ExtractorAgent extracts relevant fields.
ValidatorAgent checks for missing documents and discrepancies.
DecisionAgent produces a claim decision.
The response is returned as a JSON object per the specified schema.



AI Tool Usage
AI tools enhanced development efficiency and robustness:

Cursor.ai: Used for code scaffolding, autocompletion, and debugging in Visual Studio Code (via ms-python extension). It assisted in creating FastAPI endpoints, agent classes, and resolving LangGraph issues.
Google Gemini: Utilized via the Gemini API for prompt design, architecture suggestions, and debugging, particularly for handling malformed JSON responses.
Prompt Examples:
Classifier Prompt:Given a PDF filename and its extracted text, classify the document as either 'bill' or 'discharge_summary'.
Filename: {filename}
Text: {text}
Return ONLY a valid JSON object with a single key 'doc_type' and the document type as its value, like this:
{
  "doc_type": "bill"
}
If classification is unclear, return:
{
  "doc_type": "unknown"
}
Output MUST be valid JSON, with no extra text, no markdown, no explanations.


Extractor Prompt (Bill):Extract the following information from the bill text:
- hospital_name (string)
- total_amount (float)
- date_of_service (string, format YYYY-MM-DD)
Return a valid JSON object with these fields. Example:
{
  "hospital_name": "Example Hospital",
  "total_amount": 1234.56,
  "date_of_service": "2025-01-01"
}
Ensure the response is strictly JSON-formatted.
Text: {text}


Debugging Prompt:My FastAPI endpoint raises a 500 error with message: "Classification failed: '\\n          \"doc_type\"'". Here's the code:
{code}
The Gemini API returns malformed JSON. Suggest fixes to ensure valid JSON output.





Setup Instructions (Windows)

Create Project Directory:mkdir HealthPay
cd HealthPay


Install Dependencies:pip install -r requirements.txt

Ensure requirements.txt includes:fastapi
uvicorn[standard]
pdfplumber
python-dotenv
python-multipart
google-generativeai


Configure Environment:Create a .env file in the project root with Google Gemini API keys:GOOGLE_API_KEYS=AIzaSyBEgL6eh78wLNCoiHhh5An_nWOe5LdDSxo,AIzaSyBClgq5Vo_rfMW9rWS4MrbudEW0hgTd6GY,AIzaSyA1NP13vD3Q_S18tZ2U0HhwWdW0es5

Note: Multiple keys are provided to mitigate quota limits (429 errors). If issues persist, obtain a new key from Google AI Studio for gemini-1.5-flash (1M tokens/day, 15 requests/minute).
Run the Application:uvicorn app.main:app --reload



Testing Instructions

Manual Testing:
Download sample PDFs (sample_bill.pdf, sample_discharge.pdf) from the Google Drive link.
Use Postman to upload PDFs to the /process-claim endpoint:
Create a POST request to http://localhost:8000/process-claim.
Set body to form-data.
Add multiple files keys with PDFs (e.g., 25020500888-2_20250427_120744-ganga ram.pdf, sample_discharge.pdf).
Set Accept header to application/json.
Send and verify the JSON response matches the schema:{
  "documents": [
    {
      "type": "bill",
      "hospital_name": "string",
      "total_amount": 0.0,
      "date_of_service": "string"
    },
    {
      "type": "discharge_summary",
      "patient_name": "string",
      "diagnosis": "string",
      "admission_date": "string",
      "discharge_date": "string"
    }
  ],
  "validation": {
    "missing_documents": [],
    "discrepancies": []
  },
  "claim_decision": {
    "status": "approved",
    "reason": "All required documents present and consistent"
  }
}






Automated Testing: Not implemented due to dynamic PDF uploads. Manual testing via Postman ensures functionality.

Failures & Tradeoffs

LLM Response Inconsistency: Gemini (gemini-1.5-flash) may return malformed JSON (e.g., "doc_type"). Mitigated in classifier.py with a fallback that uses filename keywords (bill or discharge), but accuracy may decrease for unclear filenames.
LLM Quota Limits: Free-tier Gemini API may hit 429 errors (15 requests/minute or daily token cap). Multiple API keys in .env help, but a paid tier is ideal for production.
PDF Parsing: pdfplumber handles text-based PDFs well but may struggle with scanned images. OCR libraries (e.g., Tesseract) were excluded to keep dependencies light.
Error Handling: Try-catch blocks with logging capture errors. Exponential backoff for LLM retries was omitted for simplicity.
Scalability: Single-threaded FastAPI processes files sequentially. Celery could improve throughput but was not included.

Troubleshooting

500 Errors: Check uvicorn logs:
Gemini 429 Error: Quota exceeded. Rotate through the provided API keys or get a new key from Google AI Studio.
JSON Parsing Errors: Malformed Gemini output is handled by classifier.py fallback. Ensure filenames include bill or discharge.
PDF Errors: Verify PDFs are text-based (not scanned). Open in a PDF viewer to confirm.


400 Bad Request: Ensure Postman request uses correct form-data syntax and valid PDFs.
Dependency Issues: Run pip install --upgrade fastapi uvicorn pdfplumber python-dotenv python-multipart google-generativeai for compatibility.

Submission Notes

Project Structure:HealthPay/
├── app/
│   ├── agents/
│   │   ├── classifier.py
│   │   ├── extractor.py
│   │   ├── validator.py
│   │   └── decision.py
│   ├── utils/
│   │   └── pdf_reader.py
│   └── main.py
├── .env
├── README.md
├── requirements.txt


Completeness: Includes all required files: app/main.py, app/agents/ (four agents), app/utils/pdf_reader.py, requirements.txt, .env, README.md.
Testing for Reviewers: Use sample PDFs from the Google Drive link and one of the provided API keys. Test via Postman as described.
Known Issue: Malformed JSON from Gemini is handled by filename-based fallback in classifier.py, ensuring workflow completion.
