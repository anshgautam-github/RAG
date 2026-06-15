from langchain_openai import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain.document_loaders import TextLoader

## Load the documents
loader=TextLoader("langchain_intro.txt")
docs=loader.load()

## Initialize embedding model
embedding=OpenAIEmbeddings()

## Create the semantic chunker
chunker=SemanticChunker(embedding)

## Split the documents
chunks=chunker.split_documents(docs)

## Result

for i,chunk in enumerate(chunks):
    print(f"\n chunk {i+1}:\n{chunk.page_content}")