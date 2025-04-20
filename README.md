# 🧠 Enterprise Assistant

The **Enterprise Assistant** is an intelligent document analysis tool built with **Streamlit** and **Hugging Face Transformers**. It allows users to upload PDF documents, extract insights using **RAG (Retrieval-Augmented Generation)**, generate summaries, identify keywords, and interact with the document via natural language chat.

---

## 🚀 Features

- **📄 PDF Upload & Text Extraction**
  - Upload any PDF document.
  - Extracts clean, readable text using PyMuPDF.

- **💬 Chat with Your Document**
  - Ask natural questions.
  - Get context-aware answers using FAISS + Transformers (RAG).

- **🔍 Quick Analysis**
  - Generate summaries.
  - Extract important keywords.

- **📊 Advanced Tools**
  - Detailed summary generation.
  - Advanced keyword analysis using TF-IDF.

- **🧼 Input Cleaning**
  - Filters out profanity and normalizes input for better QA.

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/) – Frontend & UI
- [Transformers (Hugging Face)](https://huggingface.co/transformers/) – QA pipeline
- [SentenceTransformers](https://www.sbert.net/) – Embeddings for semantic search
- [FAISS](https://github.com/facebookresearch/faiss) – Vector similarity search
- [NLTK](https://www.nltk.org/) – Text processing
- [scikit-learn](https://scikit-learn.org/) – Keyword extraction (TF-IDF)
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) – PDF parsing

---

## 🖥️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/enterprise-assistant.git
cd enterprise-assistant
```

### 2. Install Dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

You may need the following additional NLTK resources:

```python
import nltk
nltk.download("stopwords")
nltk.download("punkt")
```

### 3. Run the App

```bash
streamlit run app.py
```

---

## 📂 File Structure

```
enterprise-assistant/
│
├── app.py                  # Streamlit UI
├── chatbot.py              # RAG-based chatbot logic
├── document_handler.py     # PDF processing, summarization, keyword extraction
├── utils.py                # Input cleaning and profanity filtering
├── bad_words.txt           # List of words to censor
├── extracted_text.txt      # Saved document text (optional)
└── requirements.txt        # Python dependencies
```

---

## ✅ Requirements

- Python 3.8+
- Streamlit
- faiss-cpu
- sentence-transformers
- transformers
- PyMuPDF
- scikit-learn
- nltk

---

## 🛡️ Privacy Notice

All processing is done **locally**. Your documents and questions are **never sent to the cloud**. This assistant is designed with enterprise privacy in mind.

---

## 📬 Future Enhancements

- Multi-document support
- Document tagging and history
- Named entity recognition (NER)
- Export analysis results

---

