"""
Transform text into vectors using TF-IDF.
"""

from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize(texts):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)
    return vectors
