from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import sys
import os
import json

# Ensure src is in the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.safety.pii_detector import detect_pii
from src.safety.intent_classifier import classify_intent, Intent
from src.safety.refusal_templates import out_of_scope_refusal, pii_rejection, advisory_refusal, performance_refusal
from src.retrieval.query_preprocessor import preprocess_query
from src.retrieval.retriever import retrieve
from src.retrieval.conflict_resolver import resolve_conflicts
from src.generation.prompt_template import build_prompt
from src.generation.generator import generate_answer_stream, generate_answer
from src.generation.response_formatter import format_response
from src.feedback.analytics import log_event

app = FastAPI(title="Mutual Fund FAQ Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    stream: bool = False

class FeedbackRequest(BaseModel):
    query: str
    response: str
    is_helpful: bool

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/feedback")
def submit_feedback(req: FeedbackRequest):
    log_event("feedback_received", {
        "query_length": len(req.query),
        "is_helpful": req.is_helpful
    })
    return {"status": "success"}

@app.post("/api/query")
def process_query(req: QueryRequest):
    query = req.query

    # 1. PII Gate
    pii_match = detect_pii(query)
    if pii_match:
        log_event("pii_blocked", {"pii_type": pii_match.pii_type, "query_length": len(query)})
        return {"response": pii_rejection(), "status": "blocked"}

    # 2. Intent Classification
    intent = classify_intent(query)
    log_event("query_received", {"intent": intent.value, "query_length": len(query)})

    if intent == Intent.ADVISORY_OPINION:
        log_event("refusal_served", {"refusal_type": "advisory"})
        return {"response": advisory_refusal(), "status": "refused"}
    elif intent == Intent.PERFORMANCE_COMPARISON:
        log_event("refusal_served", {"refusal_type": "performance"})
        return {"response": performance_refusal(), "status": "refused"}
    elif intent == Intent.OUT_OF_CORPUS:
        log_event("refusal_served", {"refusal_type": "out_of_corpus"})
        return {"response": out_of_scope_refusal(), "status": "refused"}

    # 3. Preprocess
    normalized_query, scheme_name, clarification = preprocess_query(query)
    if clarification:
        log_event("refusal_served", {"refusal_type": "clarification_needed"})
        return {"response": clarification, "status": "clarification"}

    # 4. Retrieve
    try:
        chunks = retrieve(normalized_query, scheme_name=scheme_name)
        if not chunks:
            log_event("refusal_served", {"refusal_type": "out_of_scope"})
            return {"response": out_of_scope_refusal(), "status": "out_of_scope"}
            
        # 5. Resolve Conflicts
        resolved_chunks = resolve_conflicts(chunks)
        
        # 6. Build Prompt
        prompt = build_prompt(normalized_query, resolved_chunks)

        metadata = resolved_chunks[0].get("metadata", {})
        citation_url = metadata.get("source_url", "")
        last_updated = metadata.get("last_verified_date", "Unknown")

        if req.stream:
            def iter_response():
                try:
                    stream = generate_answer_stream(prompt)
                    raw_answer = ""
                    for chunk in stream:
                        raw_answer += chunk
                        yield json.dumps({"chunk": chunk, "done": False}) + "\n"
                    final_response = format_response(raw_answer, resolved_chunks)
                    
                    log_event("answer_served", {
                        "scheme_name": scheme_name,
                        "citation_url": citation_url,
                        "retrieval_distance": resolved_chunks[0].get("distance", 0)
                    })
                    
                    yield json.dumps({"final_response": final_response, "done": True, "citation_url": citation_url, "last_updated": last_updated}) + "\n"
                except Exception as e:
                    yield json.dumps({"error": str(e), "done": True}) + "\n"
            return StreamingResponse(iter_response(), media_type="application/x-ndjson")
        else:
            raw_answer = generate_answer(prompt)
            final_response = format_response(raw_answer, resolved_chunks)
            log_event("answer_served", {
                "scheme_name": scheme_name,
                "citation_url": citation_url,
                "retrieval_distance": resolved_chunks[0].get("distance", 0)
            })
            return {
                "response": final_response,
                "citation_url": citation_url,
                "last_updated": last_updated,
                "status": "success"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
