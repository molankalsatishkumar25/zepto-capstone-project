
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Paths
BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Required local embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def main():
    # Load the local embedding model
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Create a persistent local ChromaDB client
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Create or replace the policy collection
    try:
        client.delete_collection("zepto_policies")
    except Exception:
        pass

    collection = client.create_collection(
        name="zepto_policies"
    )

    # Load the eight policy documents
    documents = []
    ids = []
    metadatas = []

    for file_path in sorted(DOCS_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        documents.append(text)
        ids.append(file_path.stem)
        metadatas.append({"source": file_path.name})

    if len(documents) != 8:
        raise ValueError(
            f"Expected 8 policy documents, but found {len(documents)}."
        )

    # Generate local embeddings
    embeddings = model.encode(
        documents,
        normalize_embeddings=True
    ).tolist()

    # Store documents, metadata, and embeddings in ChromaDB
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    # Verify the collection
    result = collection.get()

    print("Policy indexing completed successfully.")
    print(f"Documents indexed: {len(result['ids'])}")
    print(f"Collection: {collection.name}")
    print(f"Embedding model: {EMBEDDING_MODEL}")
    print(f"ChromaDB path: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
    