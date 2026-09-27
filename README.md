# Cancer text mining and term relationships

An exploratory NLP project that extracts cancer-related website text, cleans it,
builds one- through four-word vocabularies, constructs a term-document matrix,
and uses truncated SVD and cosine nearest neighbors to explore term similarity.
There is also a separate gene-symbol mapping experiment.

## Project layout

```text
notebooks/                 Numbered research pipeline, stages 01–07
  phase_2/                 Gene mapping experiment
data/
  raw/html/                Supply the crawled HTML here
  raw/reference/           Optional gene_info.csv
  interim/text/            Extracted/preprocessed text
  interim/cleaned_text/    spaCy-cleaned text
  interim/quarantine/     Preserved rejected input samples
  external/               Optional trigramStopWords.csv
  processed/ngrams/        Existing vocabulary and frequency tables
  processed/matrices/     Existing term_document_matrix.csv
results/neighbors/        Existing best_neibhours.csv (original name retained)
docs/analysis.md           Findings, limitations, and recommended corrections
docs/file_migration.json   Old/new locations and original SHA-256 hashes
project_paths.py           Shared paths anchored to this repository
requirements.txt          Dependencies observed in the notebooks
```

## Setup

The large term-document matrix is stored with Git LFS. Install Git LFS before
cloning, or run `git lfs install` and `git lfs pull` in an existing clone to
download the matrix contents.

From the project root, create a Python environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt punkt_tab stopwords wordnet
python -m jupyterlab
```

The dependencies are not version-locked; a full environment run remains to be
validated. Launch Jupyter inside this repository so notebooks can locate
`project_paths.py`. All data paths are now defined there.

## Pipeline and inputs

| Stage | Notebook | Purpose |
| --- | --- | --- |
| 0 | Not supplied | Crawl website and remove HTML boilerplate |
| 1 | `01_text_extraction.ipynb` | Detect language, extract HTML body text, apply initial NLTK cleaning |
| 2 | `02_data_cleaning.ipynb` | spaCy lemmatization, POS/entity filtering, stopwords |
| 3 | `03_ngrams.ipynb` | Count unigrams to quadgrams and document frequencies |
| 4 | `04_ngram_cleaning.ipynb` | Derive candidate stopwords and filter repeated-token grams |
| 5 | `05_frequency_adjustment.ipynb` | Historical heuristic for nested-gram frequency subtraction |
| 6 | `06_term_document_matrix.ipynb` | Count vocabulary terms across documents |
| 7 | `07_svd_neighbors.ipynb` | SVD embeddings and cosine nearest neighbors |
| Optional | `phase_2/gene_mapping.ipynb` | Match gene symbols to document IDs |

The source corpus, crawler, original HTML-cleaning code, custom stopword file,
and gene reference are absent. Existing CSVs allow inspection of previous
results, but do not establish end-to-end reproducibility.

Stage 2 now permits an initial pass without custom stopwords. Stage 4 generates
candidate stopwords; review them before repeating stages 2 and 3. Frequency
alone does not establish that a word is irrelevant. The saved trigram vocabulary
is present, but its generation cell is commented out in stage 4, so that stage
is not a complete vocabulary regeneration workflow.

**Read `docs/analysis.md` before rerunning or relying on the results.** Stage 1
moves rejected inputs into quarantine, and later stages overwrite their CSV
outputs. Work on a copy of the corpus and preserve baseline outputs before
rerunning. The organization retained historical notebook outputs and CSV bytes;
it did not regenerate the model or silently replace the research methodology.
