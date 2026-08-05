import streamlit as st
import os
import sys

# Ensure src is in the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.safety.pii_detector import detect_pii
from src.safety.intent_classifier import classify_intent, Intent
from src.safety.refusal_templates import out_of_scope_refusal
from src.retrieval.query_preprocessor import preprocess_query
from src.retrieval.retriever import retrieve
from src.retrieval.conflict_resolver import resolve_conflicts
from src.generation.prompt_template import build_prompt
from src.generation.generator import generate_answer_stream
from src.generation.response_formatter import format_response
from src.feedback.analytics import log_event
from src.scheduler.scheduler import start_scheduler

st.set_page_config(page_title="Mutual Fund FAQ Assistant", page_icon="📈")

# Start scheduler once per session
if "scheduler_started" not in st.session_state:
    start_scheduler()
    st.session_state.scheduler_started = True

st.title("Mutual Fund FAQ Assistant")
st.markdown("*Facts-only. No investment advice. Currently serving SBI Mutual Funds and Nippon India.*")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Example chips
st.markdown("**Example Queries:**")
col1, col2, col3 = st.columns(3)
if col1.button("Expense ratio of SBI Flexicap?"):
    st.session_state.example_query = "What is the expense ratio of SBI Flexicap Fund?"
if col2.button("Exit load for Nippon India Small Cap?"):
    st.session_state.example_query = "What is the exit load for Nippon India Small Cap Fund?"
if col3.button("Download capital gains statement?"):
    st.session_state.example_query = "How do I download my capital gains statement?"

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar_url = "https://upload.wikimedia.org/wikipedia/commons/4/4b/Groww_app_logo.png" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar_url):
        st.markdown(message["content"])

# React to user input
query = st.chat_input("Ask a question about mutual funds...")

if query or "example_query" in st.session_state:
    if "example_query" in st.session_state:
        query = st.session_state.example_query
        del st.session_state.example_query
        
    if not query:
        st.stop()

    # Display user message in chat message container
    st.chat_message("user").markdown(query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})

    # 1. PII Gate
    pii_match = detect_pii(query)
    if pii_match:
        from src.safety.refusal_templates import pii_rejection
        response = pii_rejection()
        log_event("pii_blocked", {"pii_type": pii_match.pii_type, "query_length": len(query)})
    else:
        # 2. Intent Classification
        intent = classify_intent(query)
        log_event("query_received", {"intent": intent.value, "query_length": len(query)})
        
        if intent == Intent.ADVISORY_OPINION:
            from src.safety.refusal_templates import advisory_refusal
            response = advisory_refusal()
            log_event("refusal_served", {"refusal_type": "advisory"})
        elif intent == Intent.PERFORMANCE_COMPARISON:
            from src.safety.refusal_templates import performance_refusal
            response = performance_refusal()
            log_event("refusal_served", {"refusal_type": "performance"})
        else:
            if "current_scheme" not in st.session_state:
                st.session_state.current_scheme = None

            # 3. Preprocess
            normalized_query, scheme_name, clarification = preprocess_query(query, st.session_state.current_scheme)
            
            if scheme_name:
                st.session_state.current_scheme = scheme_name

            if clarification:
                response = clarification
                log_event("refusal_served", {"refusal_type": "clarification_needed"})
            else:
                # 4. Retrieve
                try:
                    chunks = retrieve(normalized_query, scheme_name=scheme_name)
                    
                    if not chunks:
                        response = out_of_scope_refusal()
                        log_event("refusal_served", {"refusal_type": "out_of_scope"})
                    else:
                        # 5. Resolve Conflicts
                        resolved_chunks = resolve_conflicts(chunks)
                        
                        # 6. Build Prompt
                        prompt = build_prompt(normalized_query, resolved_chunks, scheme_name)
                        
                        # 7. Generate Answer (Streaming)
                        try:
                            stream = generate_answer_stream(prompt)
                            raw_answer = ""
                            
                            # stream display
                            with st.chat_message("assistant", avatar="https://upload.wikimedia.org/wikipedia/commons/4/4b/Groww_app_logo.png"):
                                response_placeholder = st.empty()
                                for chunk in stream:
                                    raw_answer += chunk
                                    response_placeholder.markdown(raw_answer + "▌")
                                
                                # 8 & 9. Format and Validate
                                final_response = format_response(raw_answer, resolved_chunks)
                                response_placeholder.markdown(final_response)
                                
                            response = final_response
                            skip_display = True
                            
                            log_event("answer_served", {
                                "scheme_name": scheme_name,
                                "citation_url": resolved_chunks[0].get("metadata", {}).get("source_url", "") if resolved_chunks else "",
                                "retrieval_distance": resolved_chunks[0].get("distance", 0) if resolved_chunks else 0
                            })
                        except Exception as e:
                            response = f"An error occurred while generating the answer: {str(e)}"
                except Exception as e:
                    response = f"An error occurred while retrieving information: {str(e)}\n\nPlease ensure you run the ingestion pipeline first."

    # Display assistant response in chat message container if not streamed
    if not locals().get("skip_display", False):
        with st.chat_message("assistant", avatar="https://upload.wikimedia.org/wikipedia/commons/4/4b/Groww_app_logo.png"):
            st.markdown(response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
