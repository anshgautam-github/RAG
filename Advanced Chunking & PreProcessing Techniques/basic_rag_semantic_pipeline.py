# Raw Documents
#       ↓
# Semantic Chunking
#       ↓
# Embeddings
#       ↓
# Vector Database (FAISS)
#       ↓
# Retriever
#       ↓
# User Question
#       ↓
# Similarity Search
#       ↓
# Relevant Chunks Retrieved
#       ↓
# Prompt
#       ↓
# LLM
#       ↓
# Final Answer

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chat_models import init_chat_model

# ============================================================
# RAW DOCUMENT
# ============================================================

text = """
LangChain is a framework for building applications with LLMs.

LangChain provides modular abstractions to combine LLMs
with tools, APIs, vector databases, and memory.

You can create chains, agents, retrievers, memory systems,
and prompt pipelines using LangChain.

The Eiffel Tower is located in Paris.

France is one of the world's most popular tourist destinations.

Millions of tourists visit France every year.
"""

# ============================================================
# STEP 1: SPLIT INTO SENTENCES
# ============================================================

sentences = [ s.strip() for s in text.split("\n") if s.strip() ]

# ============================================================
# STEP 2: CREATE SENTENCE EMBEDDINGS
# ============================================================

semantic_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
sentence_embeddings = semantic_model.encode(sentences)

# ============================================================
# STEP 3: SEMANTIC CHUNKING
# ============================================================

threshold = 0.60

chunks = []

current_chunk = [sentences[0]]

for i in range(1, len(sentences)):

    similarity = cosine_similarity(
        [sentence_embeddings[i - 1]],
        [sentence_embeddings[i]]
    )[0][0]

    if similarity >= threshold:

        current_chunk.append(sentences[i])

    else:

        chunks.append(
            " ".join(current_chunk)
        )

        current_chunk = [sentences[i]]

chunks.append(
    " ".join(current_chunk)
)

# ============================================================
# STEP 4: CONVERT CHUNKS TO DOCUMENTS
# ============================================================

documents = [
    Document(page_content=chunk)
    for chunk in chunks
]

# ============================================================
# STEP 5: EMBEDDING MODEL FOR VECTOR DB
# ============================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ============================================================
# STEP 6: CREATE VECTOR DATABASE
# ============================================================

vectorstore = FAISS.from_documents(
    documents,
    embedding_model
)

# ============================================================
# STEP 7: CREATE RETRIEVER
# ============================================================

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# ============================================================
# STEP 8: CREATE LLM
# ============================================================

llm = init_chat_model(model="groq:gemma2-9b-it", temperature=0.4 )

# ============================================================
# STEP 9: PROMPT TEMPLATE
# ============================================================

template = """
Answer the question ONLY from the provided context.

Context:
{context}

Question:
{input}
"""
prompt = PromptTemplate.from_template(template)

# ============================================================
# STEP 10: DOCUMENT CHAIN
# This chain: takes retrieved documents , stuffs them into prompt , sends prompt to LLM
# ============================================================

document_chain = create_stuff_documents_chain(
    llm,
    prompt
)

# ============================================================
# STEP 11: RETRIEVAL CHAIN
# This chain: takes user question , retrieves relevant chunks, passes chunks to document chain, 
# gets final answer from LLM

# ============================================================

retrieval_chain = create_retrieval_chain(
    retriever,
    document_chain
)

# ============================================================
# STEP 12: ASK QUESTION
# ============================================================

query = {
    "input": "What is LangChain used for?"
}

result = retrieval_chain.invoke(query)

# ============================================================
# STEP 13: ANSWER
# ============================================================

print("\nAnswer:\n")
print(result["answer"])