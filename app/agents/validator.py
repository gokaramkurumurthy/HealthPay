def validate(documents):
    discharge_doc = next((d for d in documents if d.get("type") == "discharge_summary"), None)
    bill_doc = next((d for d in documents if d.get("type") == "bill"), None)
    id_doc = next((d for d in documents if d.get("type") == "id_proof"), None)

    missing = []
    if not discharge_doc: missing.append("discharge_summary")
    if not bill_doc: missing.append("bill")
    if not id_doc: missing.append("id_proof")

    discrepancies = []
    if discharge_doc and bill_doc:
        if discharge_doc.get("discharge_date") != bill_doc.get("date_of_service"):
            discrepancies.append("Discharge date and billing date mismatch")

    return {"missing_documents": missing, "discrepancies": discrepancies}
