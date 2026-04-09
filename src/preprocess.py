"""
Clean text so the computer can understand it.
"""

import re
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

STOPWORDS = set(ENGLISH_STOP_WORDS)

def preprocess(text):
    text = text.lower()
    tokens = re.findall(r"\b\w+\b", text)
    tokens = [
        word for word in tokens
        if word not in STOPWORDS
        and word not in string.punctuation
    ]
    return " ".join(tokens)