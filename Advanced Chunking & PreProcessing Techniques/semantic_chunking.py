from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

## Initialize the model
model=SentenceTransformer('all-MiniLM-L6-v2')

## Sample text
text="""
LangChain is a framework for building applications with LLMs.
Langchain provides modular abstractions to combine LLMs with tools like OpenAI and Pinecone.
You can create chains, agents, memory, and retrievers.
The Eiffel Tower is located in Paris.
France is a popular tourist destination.
"""

## Step 1 : Split into sentences
sentences=[s.strip() for s in text.split("\n") if s.strip()]

### sstep 2: Embed each setence
embeddings=model.encode(sentences)

# Step 3: Initialize parameters
threshold = 0.7  # control chunk tightness
chunks = []
current_chunk=[sentences[0]] # list so we can append sentences to it until we decide to start a new chunk

## Step 4: Semantic grouping based on threshold

for i in range(1, len(sentences)):
    sim = cosine_similarity(
        [embeddings[i - 1]],
        [embeddings[i]]
    )[0][0]

    if sim>=threshold:
        current_chunk.append(sentences[i])
    else:
        chunks.append(" ".join(current_chunk))  # The new sentence does not belong to the current chunk, so close the current chunk and start a new one
        #join means:"Take all strings inside this list and join them together using a space (" ") between each one.
        current_chunk=[sentences[i]] 

# Append the last chunk
chunks.append(" ".join(current_chunk))

# Output the chunks
print("\n📌 Semantic Chunks:")
for idx, chunk in enumerate(chunks):
    print(f"\nChunk {idx+1}:\n{chunk}")




