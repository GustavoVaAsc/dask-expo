import dask
from dask.distributed import Client
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter
import pandas as pd


WORD_RE = re.compile(r'[a-z]+')


def tokenize(text):
    """Extract normalized words from text after removing HTML and URLs."""
    cleaned = re.sub(r'<[^>]+>', ' ', str(text))
    cleaned = re.sub(r'https?://\S+', ' ', cleaned)
    return [w for w in WORD_RE.findall(cleaned.lower()) if len(w) > 3]


def count_words_in_csv(path, text_columns, chunksize=20000):
    """Stream a CSV in chunks and return a Counter for selected text columns."""
    counts = Counter()

    read_iter = pd.read_csv(
        path,
        usecols=text_columns,
        dtype=str,
        chunksize=chunksize,
        engine='python',
        on_bad_lines='skip',
        encoding='utf-8',
        encoding_errors='ignore',
    )

    for chunk in read_iter:
        # Process row-by-row to keep peak memory bounded to one CSV chunk.
        for row in chunk.fillna('').itertuples(index=False, name=None):
            counts.update(tokenize(' '.join(row)))

    return counts


def merge_counters(counters):
    """Merge a sequence of Counters into one aggregate Counter."""
    merged = Counter()
    for c in counters:
        merged.update(c)
    return merged

