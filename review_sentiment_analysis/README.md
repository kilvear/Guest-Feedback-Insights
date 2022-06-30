# Review Sentiment Analysis

The goal of `sentiment_analysis_pipeline.ipynb` python notebook is to:

- Normalize raw data by date and year
- Preprocess data
- Perform sentiment classification
- Sentiment analysis

There are a few main python scripts used to reduce clutter in the notebook:

- `normalize_data.py` (Normalize date and ratings)
- `preprocess_sentiment.py` (Preprocessing steps for sentiment classification)
- `get_sentiment.py` (Get sentiment labels from the models)
- `analysis_func.py` (Visualisations for sentiment analysis)

Additional files:

- `sentiment_validation.ipynb` (Used to compare sentiment models)
- `attractions_master.xlsx` (Raw data from scraping)

Files that require personal account:

- `sdcsentiment-584f24f06d91.json`

This file is generated from the Google Cloud Platform Language API.

The link for steps to generate a new file:
(https://cloud.google.com/natural-language/docs/reference/libraries)

## Installation

Python v3.9.6 is used

Best to create a new virtual environment with requirements.txt to run the review sentiment analysis.

```bash
pip install -r requirements.txt
```

## Output

- `output/attractions_master_sentiment.xlsx` (Labeled data using sentiment model)
- In notebook there are visualisations for the attractions
- figures (Contain word clouds)
- filtered_attractions (Filtered to specific attraction)
- `output/.._highrating_neg_neu.xlsx` (Ratings above 7 with negative or neutral sentiment)
- `output/.._topwords.xlsx` (Top words)
