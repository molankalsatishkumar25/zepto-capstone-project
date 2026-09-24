import os
from typing import TypedDict

import chromadb
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END


# ============================================================
# Configuration
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "zepto_policies"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# LMS requirement:
# MOCK_LLM unset or "1" = required graded baseline
# MOCK_LLM="0" = optional real-LLM extension
MOCK_LLM = os.getenv("MOCK_LLM", "1") != "0"


# ============================================================
# Embedding model + ChromaDB
# ============================================================

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

collection = chroma_client.get_collection(
    name=COLLECTION_NAME
)


# ============================================================
# Pydantic response schema
# ============================================================

class AnswerResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)


# ============================================================
# LangGraph state
# ============================================================

class AssistantState(TypedDict, total=False):
    query: str
    intent: str
    retrieved_documents: list[str]
    retrieved_ids: list[str]
    answer: str
    sources: list[str]
    confidence: float


# ============================================================
# Structured prompt
# Required LMS skeleton:
# role + context + task + format + length
# plus negative constraint + few-shot example
# ============================================================

STRUCTURED_PROMPT = """
ROLE:
You are a Zepto customer-support assistant.

CONTEXT:
Answer only using the Zepto policy information provided in the retrieved context.

TASK:
Answer the user's policy question using the retrieved policy information.

FORMAT:
Return a concise, direct answer. Do not invent policy details.

LENGTH:
Keep the answer short and relevant, using approximately 2-4 sentences.

NEGATIVE CONSTRAINT:
Do not answer using information that is not present in the provided context.

FEW-SHOT EXAMPLE:
User question: How long do I have to report a damaged grocery item?
Context: Grocery and perishable items may be reported for a return within 24 hours of delivery if damaged, spoiled, or incorrect.
Answer: Damaged grocery items should be reported within 24 hours of delivery.

USER QUESTION:
{query}

RETRIEVED CONTEXT:
{context}
"""


# ============================================================
# classify_intent
# ============================================================

def classify_intent(state: AssistantState) -> AssistantState:
    query = state["query"].lower()

    policy_keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours",
    ]

    if any(keyword in query for keyword in policy_keywords):
        intent = "policy_question"
    else:
        intent = "general_question"

    return {
        **state,
        "intent": intent,
    }


# ============================================================
# retrieve_and_answer
# ============================================================

def retrieve_and_answer(state: AssistantState) -> AssistantState:
    query = state["query"]

    # Create query embedding locally.
    query_embedding = embedding_model.encode(
        [query]
    )[0].tolist()

    # LMS requirement: retrieve top 3 chunks.
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas"],
    )

    documents = results.get("documents", [[]])[0]
    ids = results.get("ids", [[]])[0]

    if not documents:
        return {
            **state,
            "retrieved_documents": [],
            "retrieved_ids": [],
            "answer": "No relevant Zepto policy information was found.",
            "sources": [],
            "confidence": 0.0,
        }

    # Required mock-mode behavior:
    # use a short excerpt from the most similar chunk.
    top_chunk = documents[0]
    top_chunk_snippet = top_chunk[:200]

    if MOCK_LLM:
        answer = (
            f"Based on the retrieved context: "
            f"{top_chunk_snippet}"
        )
    else:
        # Optional real-LLM extension.
        # The required graded baseline does not use this branch.
        answer = generate_real_llm_answer(
            query=query,
            documents=documents,
        )

    return {
        **state,
        "retrieved_documents": documents,
        "retrieved_ids": ids,
        "answer": answer,
        "sources": ids,
        "confidence": 1.0,
    }


# ============================================================
# direct_answer
# ============================================================

def direct_answer(state: AssistantState) -> AssistantState:

    if MOCK_LLM:
        answer = (
            "I can only answer questions about Zepto policies right now."
        )
    else:
        answer = generate_real_llm_answer(
            query=state["query"],
            documents=[],
        )

    return {
        **state,
        "answer": answer,
        "sources": [],
        "confidence": 1.0,
    }


# ============================================================
# Optional real-LLM extension
# ============================================================

def generate_real_llm_answer(
    query: str,
    documents: list[str],
) -> str:
    """
    Optional MOCK_LLM=0 extension.

    The graded baseline uses MOCK_LLM=1 and never calls
    an external LLM.
    """

    context = "\n\n".join(documents)

    prompt = STRUCTURED_PROMPT.format(
        query=query,
        context=context,
    )

    # Placeholder for optional real LLM integration.
    # The required LMS mock mode does not execute this function.
    raise RuntimeError(
        "Real LLM mode is optional and is not enabled in the "
        "required MOCK_LLM baseline."
    )


# ============================================================
# Conditional routing
# ============================================================

def route_after_classification(state: AssistantState) -> str:

    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


# ============================================================
# Build LangGraph
# ============================================================

graph_builder = StateGraph(AssistantState)

graph_builder.add_node(
    "classify_intent",
    classify_intent,
)

graph_builder.add_node(
    "retrieve_and_answer",
    retrieve_and_answer,
)

graph_builder.add_node(
    "direct_answer",
    direct_answer,
)

graph_builder.set_entry_point("classify_intent")

graph_builder.add_conditional_edges(
    "classify_intent",
    route_after_classification,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer",
    },
)

graph_builder.add_edge(
    "retrieve_and_answer",
    END,
)

graph_builder.add_edge(
    "direct_answer",
    END,
)

assistant_graph = graph_builder.compile()


# ============================================================
# Public function used by FastAPI later
# ============================================================

def ask_assistant(query: str) -> AnswerResponse:

    state: AssistantState = {
        "query": query,
    }

    result = assistant_graph.invoke(state)

    response = AnswerResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 1.0),
    )

    return response


# ============================================================
# Local test
# ============================================================

if __name__ == "__main__":

    print("MOCK_LLM:", "1" if MOCK_LLM else "0")
    print()

    policy_query = "What is the delivery time for my order?"

    print("Policy question:")
    print(policy_query)

    response_1 = ask_assistant(policy_query)

    print("Response:")
    print(response_1.model_dump_json(indent=2))

    print()
    print("-" * 60)
    print()

    general_query = "What is the capital of India?"

    print("General question:")
    print(general_query)

    response_2 = ask_assistant(general_query)

    print("Response:")
    print(response_2.model_dump_json(indent=2))
