import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# ─── Global Models ─────────────────────────────────────────────────────────────
# Embedding model
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBED_MODEL_NAME)

# QA pipeline
qa_pipeline = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2",
    tokenizer="deepset/roberta-base-squad2"
)

# ─── Helpers ────────────────────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    """Normalize whitespace."""
    return re.sub(r"\s+", " ", text).strip()

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list[str]:
    """
    Split `text` into overlapping chunks of roughly `chunk_size` words,
    overlapping by `chunk_overlap` words.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - chunk_overlap
    return chunks

def build_faiss_index(chunks: list[str]) -> faiss.IndexFlatL2:
    """
    Given a list of text chunks, embed them and build a FAISS index.
    """
    embeddings = embedder.encode(chunks, convert_to_tensor=False)
    embeddings = np.array(embeddings, dtype="float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

# ─── Main RAG Function ─────────────────────────────────────────────────────────
def get_response_from_rag(question: str, document_text: str, top_k: int = 5) -> str:
    """
    1. Clean the question.
    2. Chunk the document.
    3. Build or update FAISS index.
    4. Embed the question and retrieve top_k chunks.
    5. Run HF QA pipeline over the concatenated chunks.
    """
    try:
        q = clean_text(question)
        # 1. Chunk document
        chunks = chunk_text(document_text)
        if not chunks:
            return "❌ Document is empty or too short."

        # 2. Build FAISS index
        index = build_faiss_index(chunks)

        # 3. Embed question & search
        q_emb = embedder.encode([q], convert_to_tensor=False)
        q_emb = np.array(q_emb, dtype="float32")
        distances, indices = index.search(q_emb, top_k)

        # 4. Gather top chunks as context
        retrieved = []
        for idx in indices[0]:
            if 0 <= idx < len(chunks):
                retrieved.append(chunks[idx])
        context = " ".join(retrieved)

        if not context.strip():
            return "❌ Could not retrieve any relevant context."

        # 5. Ask the QA pipeline
        result = qa_pipeline(question=q, context=context)
        answer = result.get("answer", "").strip()
        return answer or "❌ I couldn't find an answer based on the document."

    except Exception as e:
        return f"❌ Error: {e}"
