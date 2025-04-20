import os
import re

# Load bad words from the specified file
def load_bad_words(filepath="bad_words.txt"):
    if not os.path.exists(filepath):
        return []
    
    try:
        with open(filepath, "r") as file:
            return {line.strip().lower() for line in file.readlines()}  # Using set for faster lookups
    except Exception as e:
        raise Exception(f"Error loading bad words from file: {e}")

# Clean input text by removing extra spaces and censoring bad words
def clean_input(text: str, bad_words: set) -> str:
    try:
        text = re.sub(r"\s+", " ", text).strip()
        
        for word in bad_words:
            pattern = r"\b" + re.escape(word) + r"\b"
            text = re.sub(pattern, "[CENSORED]", text, flags=re.IGNORECASE)
        
        return text
    except Exception as e:
        return f"❌ Error cleaning input text: {e}"
