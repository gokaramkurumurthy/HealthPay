from fastapi import FastAPI, UploadFile, File
from typing import List
from app.utils.pdf_reader import extract_text_from_pdf
from app.agents.classifier import classify
from app.agents.extractor import extract
from app.agents.validator import validate
from app.agents.decision import decide

app = FastAPI(title="Claim Processor")

@app.post("/process-claim")
async def process_claim(files: List[UploadFile] = File(...)):
    documents = []
    for file in files:
        content = await file.read()
        text = extract_text_from_pdf(content)
        doc_type = classify(text, file.filename)
        data = extract(doc_type, text)
        documents.append(data)

    validation = validate(documents)
    decision = decide(documents, validation)

    return {
        "documents": documents,
        "validation": validation,
        "claim_decision": decision
    }
