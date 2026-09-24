# Module 3 - Zepto Support Assistant

## 1. Objective

This module implements a retrieval-augmented support assistant for Zepto customer-policy questions.

The assistant uses the provided policy documents as its knowledge base and is designed to retrieve relevant policy information before generating an answer.

## 2. Policy Documents

The knowledge base contains the following eight policy documents:

- `doc_01_delivery.txt`
- `doc_02_returns_refunds.txt`
- `doc_03_membership.txt`
- `doc_04_order_tracking.txt`
- `doc_05_cancellation.txt`
- `doc_06_damaged_missing.txt`
- `doc_07_gift_cards.txt`
- `doc_08_support_hours.txt`

## 3. System Architecture

The Zepto Support Assistant uses a retrieval-augmented workflow for answering policy-related customer questions.

The main components are:

- Policy documents stored as local text files.
- Local sentence-transformer embeddings using `all-MiniLM-L6-v2`.
- ChromaDB for local vector storage and similarity search.
- LangGraph for intent classification, retrieval, and answer generation.
- Pydantic for structured API responses.
- FastAPI for exposing the `/ask` endpoint.
- Dockerfile for containerized deployment.

The workflow is:

`User Query → Intent Classification → Policy Retrieval / Direct Answer → Structured Response`
## 4. Embeddings and Vector Database

The policy documents are indexed locally using the `all-MiniLM-L6-v2` sentence-transformer model.

ChromaDB is used as the local vector database.

The indexing process:

1. Reads the eight policy documents.
2. Creates embeddings locally using `all-MiniLM-L6-v2`.
3. Stores the document text and embeddings in ChromaDB.
4. Uses similarity search to retrieve relevant policy content for policy-related questions.

The vector database is stored locally under:

`chroma_db/`
## 5. Prompt Design

The assistant uses a structured prompt approach for generating policy-based answers.

The prompt follows these components:

- **Role:** Zepto customer-support assistant.
- **Context:** Retrieved policy information from the local knowledge base.
- **Task:** Answer the customer's question using the available policy context.
- **Format:** Provide a concise and helpful response.
- **Length:** Keep the response focused and easy to understand.
- **Negative constraint:** Do not invent policy information or provide unsupported claims.

For policy questions, the retrieved policy context is used before generating the answer. For general questions, the assistant uses the direct-answer path.

## 6. LangGraph Workflow

The assistant workflow is implemented using LangGraph `StateGraph` with a typed `AssistantState`.

The graph contains three main nodes:

- `classify_intent`
- `retrieve_and_answer`
- `direct_answer`

The `classify_intent` node uses a keyword-based heuristic to determine whether the query is a policy question.

For policy questions, the workflow routes to `retrieve_and_answer`, which performs retrieval from ChromaDB and generates a response from the retrieved context.

For general questions, the workflow routes to `direct_answer`.

The workflow uses conditional routing after intent classification and terminates after the selected answer node.

## 7. API and Structured Response

The support assistant is exposed through a FastAPI endpoint:

`POST /ask`

The request accepts a customer question in the following format:

```json
{
  "query": "What is the delivery time for my order?"
}

##8. Testing

The assistant was tested through the FastAPI `/ask` endpoint.

A policy-related question successfully returned:

- An answer generated from retrieved policy context
- Retrieved source document names
- A confidence value

A general question was also tested and returned the direct-answer response path.

##9. Docker Deployment

A `Dockerfile` is included for containerized deployment of the FastAPI support assistant.

The container:

- Uses Python 3.11
- Installs the dependencies from `requirements.txt`
- Exposes port `8000`
- Starts the FastAPI application using Uvicorn

The application is configured to run on:

`http://0.0.0.0:8000`

##10. Files in This Module

```text
support_assistant/
├── docs/
│   ├── doc_01_delivery.txt
│   ├── doc_02_returns_refunds.txt
│   ├── doc_03_membership.txt
│   ├── doc_04_order_tracking.txt
│   ├── doc_05_cancellation.txt
│   ├── doc_06_damaged_missing.txt
│   ├── doc_07_gift_cards.txt
│   └── doc_08_support_hours.txt
├── chroma_db/
├── api.py
├── main.py
├── index_documents.py
├── Dockerfile
├── requirements.txt
└── README.md

##11. RAG Architecture

The Support Assistant follows this pipeline:

**Ingestion → Embedding → Retrieval → Generation**

- **Ingestion:** `index_documents.py` loads the 8 Zepto policy documents from `docs/`.
- **Embedding:** `index_documents.py` uses `all-MiniLM-L6-v2` to create local embeddings.
- **Storage/Retrieval:** ChromaDB stores the embeddings and retrieves the top-3 most similar chunks for policy questions.
- **Generation:** `main.py` uses the LangGraph nodes `classify_intent`, `retrieve_and_answer`, and `direct_answer`.
- **MOCK_LLM:** With the default mock mode, the required deterministic responses are generated without an LLM API call. If `MOCK_LLM=0` is used, the optional real-LLM generation path is used.

##12. Example API Calls

### Policy question

```text
POST /ask
{"query":"What is the delivery time for my order?"}

### Policy response

```json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard del",
  "sources": [
    "doc_01_delivery",
    "doc_02_returns_refunds",
    "doc_06_damaged_missing"
  ],
  "confidence": 1.0
}
### General question

```text
POST /ask
{"query":"What is the capital of India?"}

### General response

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```



