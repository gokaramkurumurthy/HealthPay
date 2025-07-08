def decide(docs, validation):
    if validation["missing_documents"] or validation["discrepancies"]:
        return {
            "status": "rejected",
            "reason": "Missing documents or data inconsistency"
        }
    return {
        "status": "approved",
        "reason": "All required documents present and data is consistent"
    }
