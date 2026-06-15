from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from langchain.chat_models import init_chat_model


# ============================================================
# CUSTOM SEMANTIC CHUNKER
# ============================================================

class ThresholdSemanticChunker:

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2",
        threshold=0.7
    ):
        self.model = SentenceTransformer(model_name)
        self.threshold = threshold

    def split(self, text: str):

        sentences = [
            s.strip()
            for s in text.split(".")
            if s.strip()
        ]

        if len(sentences) == 0:
            return []

        embeddings = self.model.encode(sentences)

        chunks = []
        current_chunk = [sentences[0]]

        for i in range(1, len(sentences)):

            sim = cosine_similarity(
                [embeddings[i - 1]],
                [embeddings[i]]
            )[0][0]

            if sim >= self.threshold:

                current_chunk.append(
                    sentences[i]
                )

            else:

                chunks.append(
                    ". ".join(current_chunk) + "."
                )

                current_chunk = [
                    sentences[i]
                ]

        chunks.append(
            ". ".join(current_chunk) + "."
        )

        return chunks

    def split_documents(self, docs):

        result = []

        for doc in docs:

            chunks = self.split(
                doc.page_content
            )

            for chunk in chunks:

                result.append(
                    Document(
                        page_content=chunk,
                        metadata=doc.metadata
                    )
                )

        return result


# ============================================================
# LOAD DOCUMENT
# ============================================================

loader = TextLoader(
    "data.txt",
    encoding="utf-8"
)

documents = loader.load()


# ============================================================
# SEMANTIC CHUNKING
# ============================================================

chunker = ThresholdSemanticChunker(
    threshold=0.70
)

chunked_docs = chunker.split_documents(
    documents
)

print(f"\nTotal Chunks: {len(chunked_docs)}")

for i, doc in enumerate(chunked_docs[:5]):
    print(f"\nChunk {i+1}")
    print(doc.page_content)


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# VECTOR STORE
# ============================================================

vectorstore = FAISS.from_documents(
    chunked_docs,
    embedding_model
)


# ============================================================
# RETRIEVER
# ============================================================

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3
    }
)


# ============================================================
# LLM
# ============================================================

llm = init_chat_model(
    model="groq:gemma2-9b-it",
    temperature=0.4
)


# ============================================================
# PROMPT
# ============================================================

template = """
Answer the question using ONLY the provided context.

Context:
{context}

Question:
{input}
"""

prompt = PromptTemplate.from_template(
    template
)


# ============================================================
# DOCUMENT CHAIN
# ============================================================

document_chain = create_stuff_documents_chain(
    llm,
    prompt
)


# ============================================================
# RETRIEVAL CHAIN
# ============================================================

retrieval_chain = create_retrieval_chain(
    retriever,
    document_chain
)


# ============================================================
# CHAT LOOP
# ============================================================

while True:

    question = input(
        "\nAsk Question (type 'exit' to quit): "
    )

    if question.lower() == "exit":
        break

    result = retrieval_chain.invoke(
        {
            "input": question
        }
    )

    print("\nAnswer:\n")
    print(result["answer"])