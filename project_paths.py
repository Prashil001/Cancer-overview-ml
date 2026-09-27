"""Shared repository-relative paths for the research notebooks."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
HTML_DIR = DATA_DIR / "raw" / "html"
TEXT_DIR = DATA_DIR / "interim" / "text"
CLEANED_TEXT_DIR = DATA_DIR / "interim" / "cleaned_text"
BAD_HTML_DIR = DATA_DIR / "interim" / "quarantine" / "bad_html"
OTHER_LANGUAGE_DIR = DATA_DIR / "interim" / "quarantine" / "other_lang_html"
NGRAM_DIR = DATA_DIR / "processed" / "ngrams"
MATRIX_FILE = DATA_DIR / "processed" / "matrices" / "term_document_matrix.csv"
NEIGHBORS_FILE = PROJECT_ROOT / "results" / "neighbors" / "best_neibhours.csv"
STOPWORDS_FILE = DATA_DIR / "external" / "trigramStopWords.csv"
GENE_FILE = DATA_DIR / "raw" / "reference" / "gene_info.csv"


def ensure_directories():
    for directory in (
        HTML_DIR, TEXT_DIR, CLEANED_TEXT_DIR, BAD_HTML_DIR,
        OTHER_LANGUAGE_DIR, NGRAM_DIR, MATRIX_FILE.parent,
        NEIGHBORS_FILE.parent, STOPWORDS_FILE.parent, GENE_FILE.parent,
    ):
        directory.mkdir(parents=True, exist_ok=True)
