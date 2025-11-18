
Produces natural, context-preserving chunks.

</details>

---

<a name="10"></a>
## 10. Is metadata embedded along with the text?

<details>
<summary>Answer — click to expand</summary>

No.

Only text (`page_content`) is embedded.  
Metadata stays separate for filtering, provenance, and context.

Embedding metadata would pollute semantic meaning.

</details>

---

<a name="11"></a>
## 11. What is the output type of a LangChain loader?

<details>
<summary>Answer — click to expand</summary>

A list of **Document** objects, each containing:

- `page_content`  
- `metadata`

Metadata varies by loader.

</details>

---

<a name="12"></a>
## 12. What metadata fields can a user add?

<details>
<summary>Answer — click to expand</summary>

Common metadata you can add:

- `source` (filename or URL)  
- `page` / `page_number`  
- `author`  
- `section`  
- `created_date`  
- `language`  
- `document_type` (policy, blog, article)  
- `tenant_id`  
- `ocr_confidence`  

Metadata supports filtering and transparency.

</details>

---

<a name="13"></a>
## 13. Why is it dangerous to embed an entire PDF without chunking?

<details>
<summary>Answer — click to expand</summary>

Embedding a whole PDF as one chunk is bad because:

- Topics get mixed → blurry embedding  
- Text may exceed token limits  
- Wasteful computation  
- No page-level accuracy  
- Poor retrieval → entire document returned  

**In short:**  
Large chunk = messy, inaccurate retrieval.  
Small chunk = clear meaning, better results.

</details>

---

<a name="14"></a>
## 14. When should I use different chunking styles?

<details>
<summary>Answer — click to expand</summary>

### **Character-based**
Use when text is clean and you want simple fixed cuts.

### **Recursive (hierarchical)**
Use for structured docs (PDFs, manuals, reports).  
Best accuracy.

### **Token-based**
Use when exact token control matters (embeddings or LLM limits).

**In short:**  
- Character → simple  
- Recursive → best  
- Token-based → most precise

</details>

---

<a name="15"></a>
## 15. Why does recursive splitting produce more meaningful chunks?

<details>
<summary>Answer — click to expand</summary>

It splits using larger boundaries first (paragraph → sentence → word → char).  
This preserves coherence and keeps ideas intact.

Better chunks → better embeddings.

</details>

---

<a name="16"></a>
## 16. Trade-offs of large vs small chunk sizes

<details>
<summary>Answer — click to expand</summary>

### **Large chunks**
Pros: more context, fewer vectors, cheaper search  
Cons: topic mixing, token limits, less accurate retrieval

### **Small chunks**
Pros: precise retrieval, page-level accuracy  
Cons: more vectors, more compute, may lose context

Best practice → medium chunk size (200–500 tokens)

</details>

---

<a name="17"></a>
## 17. What metadata do common loaders return?

<details>
<summary>Answer — click to expand</summary>

### **1. PDF loaders**
- `source`, `page`, `total_pages`, `title`, `author`, `size`

### **2. HTML/Web loaders**
- `url`, `title`, `description`, `lang`, `html_path`, `last_modified`

### **3. DOCX loaders**
- `source`, `style`, `section`, `author`, `created_at`

### **4. Text loaders**
- `source`, `encoding`, `file_extension`

### **5. OCR loaders**
- `ocr_confidence`, `image_size`, `page_number`

### **6. CSV/Excel loaders**
- `row`, `column`, `sheet_name`

### **7. JSON loaders**
- `key_path`, `record_index`, `schema`

Different file formats = different metadata.

</details>

---
