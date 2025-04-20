import fitz  # PyMuPDF
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import heapq

# Download necessary NLTK resources
nltk.download("stopwords")
nltk.download("punkt")

# Extract text from the uploaded PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        return None  # Return None in case of an error

# Summarize the extracted text using the frequency of words in sentences
def summarize_text(text, num_sentences=5):
    try:
        # Clean the text
        text = re.sub(r'\s+', ' ', text).strip()

        # Stopwords for filtering
        stop_words = set(stopwords.words("english"))
        words = nltk.word_tokenize(text)

        # Frequency table for words
        freq_table = {}
        for word in words:
            word = word.lower()
            if word not in stop_words and word.isalnum():
                freq_table[word] = freq_table.get(word, 0) + 1

        # Sentence scoring based on frequency table
        sentences = nltk.sent_tokenize(text)
        sentence_score = {}
        for sentence in sentences:
            for word in freq_table:
                if word in sentence.lower():
                    sentence_score[sentence] = sentence_score.get(sentence, 0) + freq_table[word]

        # Select top 'num_sentences' based on score
        summary_sentences = heapq.nlargest(num_sentences, sentence_score, key=sentence_score.get)
        return " ".join(summary_sentences)
    except Exception as e:
        return f"❌ Error summarizing text: {e}"

# Extract the top N keywords from the text using TF-IDF
def extract_keywords(text, top_n=10):
    try:
        # Vectorizing text with TF-IDF
        vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n)
        X = vectorizer.fit_transform([text])
        return vectorizer.get_feature_names_out()
    except Exception as e:
        return f"❌ Error extracting keywords: {e}"

# Save extracted text to a file
def save_extracted_text(text, filename="extracted_text.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        return f"✅ Text saved successfully to {filename}"
    except Exception as e:
        return f"❌ Error saving text: {e}"
