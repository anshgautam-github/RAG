# The goal is:
Take a large text. 
Understand the meaning of each sentence using embeddings
Compare neighboring sentences semantically.
Group related sentences together into chunks



# The overall flow -> 

Raw Text
   ↓
Split into sentences
   ↓
Convert each sentence into embeddings
   ↓
Compare neighboring sentence embeddings
   ↓
If similarity high → same chunk
If similarity low → new chunk
   ↓
Final semantic chunks



# When this line runs: model=SentenceTransformer(...)

Internally:

Download model weights
↓
Load tokenizer
↓
Load transformer network
↓
Load pooling layer
↓
Prepare inference pipeline



# text.split("\n") -> Produces: u can see empty strings

[
 "",
 "LangChain is a framework...",
 "Langchain provides modular abstractions...",
 "",
 "The Eiffel Tower is located in Paris.",
 ...
]



# embeddings=model.encode(sentences) -> WHAT HAPPENS INTERNALLY?

For EACH sentence:

Sentence
   ↓
Tokenizer
   ↓
Token IDs
   ↓
Transformer layers
   ↓
Contextual embeddings
   ↓
Pooling
   ↓
Final sentence embedding




# OUTPUT SHAPE : cosine_similarity() returns matrix.
Example: [[0.83]] Because: 1 vector compared with 1 vector
WHY [0][0] ? Extract scalar value.

# EXAMPLE SIMILARITIES
Sentence1 ↔ Sentence2 = 0.89
Sentence2 ↔ Sentence3 = 0.84
Sentence3 ↔ Sentence4 = 0.22
Sentence4 ↔ Sentence5 = 0.81


# LIMITATION 1 — ONLY COMPARES ADJACENT SENTENCES

Current logic: Sentence(i-1) vs Sentence(i)
But sometimes: sentence 3 relates to sentence 1 not sentence 2

Production systems often:compare against entire chunk centroid

# LIMITATION 2 — NO TOKEN LIMIT CONTROL
Chunks can become huge. Production RAG systems: also enforce token/window limits

# LIMITATION 3 — SIMPLE SENTENCE SPLITTING
Using: split("\n") Not robust. Real systems use: spaCy nltk syntactic parsers
to properly detect sentences.

# LIMITATION 4 — STATIC THRESHOLD
Fixed: 0.7 But optimal threshold varies by: domain embedding model text style
Advanced systems use: adaptive thresholds