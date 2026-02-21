# Voice Research Agent — Multi-Agent, Search-Based RAG System

## Overview

The **Voice Research Agent** is a local, voice-driven research assistant built using a **multi-agent architecture** and a **search-based Retrieval-Augmented Generation (RAG)** pipeline.  
The system is designed to handle real-world speech input, ambiguous queries, and factual uncertainty while maintaining transparency and user control.

Unlike standard chatbot implementations, this project focuses on **agent orchestration, safety validation, and robustness under imperfect inputs**, rather than purely on model responses.

---

## Working Screenshots

### Standby
![Standby UI](images/Standby%20process.png)

### Listening
![Listening](images/Listening%20Process.png)

### Processing
![Processing](images/Processing%20Process.png)

### Speaking
![Speaking](images/Speaking%20Process.png)

## Key Objectives

- Build a **voice-first AI system** that can operate reliably under noisy and incomplete speech input.
- Design a **modular multi-agent pipeline** with clear separation of responsibilities.
- Ensure responses are **grounded in external sources** rather than model hallucination.
- Provide **transparent system behavior** through explicit confidence scoring and UI state visualization.
- Emphasize **local execution and correctness** over cloud deployment complexity.

---

## System Architecture

The system is composed of four coordinated agents:

### 1. Planner Agent
- Interprets user intent from transcribed speech.
- Resolves conversational context (e.g., pronouns and follow-up questions).
- Performs early input validation to block vague or incomplete queries before they propagate.

### 2. Researcher Agent
- Retrieves relevant information from live external sources:
  - Wikipedia
  - Web search
  - ArXiv
- Aggregates retrieved content into a structured research payload.

### 3. Brain Agent
- Synthesizes retrieved research into a concise, spoken response.
- Enforces attribution requirements for factual claims.
- Applies domain-specific disclaimers for sensitive topics (medical, financial, legal).

### 4. Gatekeeper Agent
- Evaluates the reliability and coverage of retrieved sources.
- Computes a confidence score based on source diversity and relevance.
- Blocks or downgrades responses when information quality is insufficient.

This agent separation ensures **explainability, safety, and extensibility**.

---

## Retrieval-Augmented Generation (RAG)

This project implements a **search-based RAG approach**:

- Retrieval is performed using **live search**, not static embeddings.
- Retrieved content is injected directly into the generation prompt.
- This design prioritizes **freshness and factual grounding** over vector similarity.

The approach avoids reliance on vector databases while still satisfying the core RAG principle:
> *Generation is explicitly augmented by retrieved external knowledge.*

---

## Voice Interface and UX Design

- Uses the **Web Speech API** for client-side speech recognition and synthesis.
- Explicit UI state transitions:
  - Listening
  - Processing
  - Speaking
  - Standby
- Implements **input sanity checks** to discard accidental or partial speech.
- Provides **user-controlled cancellation**, allowing users to stop processing mid-flow.

The interface is designed as a **“glass-box” system**, making internal states visible rather than opaque.

---

## Robustness and Safety Mechanisms

The system addresses common real-world AI failure modes:

- **Incomplete voice input**  
  → Blocked via frontend transcript validation.

- **Ambiguous or underspecified queries**  
  → Stopped early at the Planner level with clarification prompts.

- **Unsafe or speculative requests**  
  → Filtered through the Gatekeeper with confidence-based blocking.

- **Unwanted responses after user cancellation**  
  → Prevented via UI-level abort handling.

These safeguards ensure the system fails **gracefully and predictably**.

---

## Technology Stack

- **Backend:** FastAPI
- **Agents & Orchestration:** Custom multi-agent pipeline
- **Retrieval:** Wikipedia API, Web search, ArXiv
- **LLM Inference:** Groq (LLaMA-3.x)
- **Frontend:** HTML, CSS, JavaScript
- **Speech:** Web Speech API (client-side)

---

## Design Decisions

- **Local-only execution:**  
  Chosen to prioritize correctness, latency, and browser-native speech handling over deployment complexity.

- **No vector database:**  
  Search-based RAG was selected to keep retrieval transparent and current.

- **Confidence as qualitative signal:**  
  Confidence is presented as High / Medium / Low instead of raw scores to avoid misleading precision.

---

## Project Impact

- Demonstrates **end-to-end ownership** of an AI system, from UI to backend to agent logic.
- Showcases **agentic system design** beyond single-prompt chatbots.
- Addresses practical AI concerns such as safety, hallucination control, and user intent validation.
- Serves as a foundation for future extensions (vector-based RAG, streaming, deployment).

---

## Status

This project is intentionally maintained as a **local application** for experimentation, learning, and architectural clarity.
