from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.schema import Document

# Sample docs
docs = [
    Document(page_content="LangChain helps build LLM applications."),
    Document(page_content="Pinecone is a vector database for semantic search."),
    Document(page_content="The Eiffel Tower is located in Paris."),
    Document(page_content="LangChain can be used to develop agentic ai applications."),
    Document(page_content="lancha has many types of retrievers."),
]

#Dense Retriever
embedding_model = HuggingFaceEmbeddings(model_name="all-MINI-L6-v2")
dense_vectorstore = FAISS.from_documents(docs,embedding_model)
dense_retriever = dense_vectorstore.as_retriever()