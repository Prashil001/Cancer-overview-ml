# Repository analysis

## What is implemented

The supplied code implements exploratory, unsupervised term similarity. Terms
are rows and documents are columns of a count matrix. Truncated SVD reduces the
document dimensions, and `NearestNeighbors` ranks other term vectors by cosine
distance. This is nearest-neighbor retrieval, not a supervised KNN classifier.
The similarities describe corpus usage, not established biological relationships.

The crawler and explicit header/footer removal are not in this repository.
The extraction notebook reads all HTML body text without removing navigation,
scripts, styles, headers, or footers itself. Earlier external cleaning may have
handled these elements, but that cannot be verified here.

## Observed artifacts

| Artifact | Data rows | Notes |
| --- | ---: | --- |
| unigram_sorted.csv | 29,439 | Original unigram counts |
| goodBigram.csv | 297,477 | Bigram vocabulary |
| goodTriGrams.csv | 240 | Saved selected trigrams |
| goodQuadgram.csv | 55 | Includes an extra unnamed index column |
| goodUni_cleaned.csv | 9,167 | 84 negative total frequencies |
| goodbi_cleaned.csv | 28,506 | 2 negative total frequencies |
| term_document_matrix.csv | 37,968 | 2,285 document columns plus term name; about 174 MB |
| best_neibhours.csv | 379,680 | Ten saved neighbors per term on average |

The vocabulary sizes sum to 37,968, matching the matrix row count. The original
files `bad_html` and `other_lang_html` were regular files, despite code treating
those names as directories. The former has a JPEG-like byte prefix; the latter
begins with Spanish HTML. Both have been preserved inside quarantine directories.

## Issues affecting results

1. **Substring counting:** stage 6 uses `str.count`, so a unigram can match
   inside a longer word, and overlapping phrase occurrences are missed. Replace
   this with token-window counting before rebuilding the matrix.
2. **Incorrect frequency adjustment:** stage 5 deduplicates subgrams while keeping
   only their first parent; it mixes positional iteration with `.loc` labels
   after filtering rows; and the bigram subtraction section reuses the lists
   built from trigrams. This can update the wrong rows or create new ones.
   Negative frequencies are already present in saved outputs. `avg` and
   `documents` are not recomputed after changing totals. Prefer original counts
   until a clearly defined, document-level overlap policy is implemented.
3. **Adjusted counts are not matrix weights:** stage 6 uses stage 5 tables only
   as vocabulary lists and recounts text. Adjusting their frequency columns does
   not directly change SVD inputs, although vocabulary corruption can affect it.
4. **Aggressive cleaning:** extraction first runs NLTK cleaning, then stage 2
   applies spaCy to the already altered text. Removed words and sentence breaks
   can make later ngrams artificial and reduce POS/NER quality. Keep an untouched
   extracted-text layer and generate phrases within sentence boundaries.
5. **Custom stopwords:** updating spaCy's `STOP_WORDS` after loading the model
   does not reliably update existing lexemes' `is_stop` flags. Explicitly test
   token/lemma membership or update lexeme flags. Stage 4 splits frequent phrases
   into individual stopwords, which can remove meaningful cancer terminology.
6. **Missing provenance:** document columns are numbered from an unsorted glob,
   with no persisted ID-to-filename/URL map. Gene mapping separately repeats this
   enumeration. Save a shared, sorted document manifest before regenerating.
7. **Neighbor self-exclusion:** dropping the first neighbor assumes it is the
   query itself. Tied vectors can violate that assumption. Exclude the query by
   its actual row index, and explicitly handle zero vectors.
8. **Model evaluation:** raw counts emphasize frequent terms. Compare a defined
   TF-IDF baseline, bound SVD dimensions to input size, inspect zero vectors,
   and evaluate against reviewed term pairs. Explained variance alone does not
   establish semantic quality. No reviewed evaluation set is included.
9. **Gene mapping:** lowercased exact symbols can be ambiguous ordinary words;
   short symbols may already have been removed by the length filter. The gene
   reference and species/version provenance are missing.

## Changes made during organization

- Numbered and grouped notebooks; separated corpus stages, vocabulary tables,
  matrix, and neighbor results. Retained the separate phase 2 experiment.
- Centralized active file paths in `project_paths.py`, including quarantine.
- Preserved current working-copy content, including the previously modified SVD
  notebook and previously untracked matrix, neighbors, and phase 2 notebook.
- Removed a standalone `+` syntax error in SVD and corrected a three-argument
  call to the two-argument `cleanNgram` function.
- Added the NLTK `punkt_tab` download and made initial custom stopwords optional
  to permit bootstrapping. Historical outputs remain historical.
- Left methodological issues above explicit rather than silently changing the
  experiment and presenting old outputs as newly validated results.

## Validation limits

CSV sizes, headers, row counts, and negative frequencies were inspected directly.
Organization verification checks preserved artifact hashes, parses notebook
JSON, and compiles code cells after excluding notebook magic lines. Full notebook
execution and scientific validation require the missing corpus and dependencies.
