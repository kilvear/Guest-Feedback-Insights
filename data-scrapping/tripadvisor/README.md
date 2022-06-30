# TripAdvisor Scrapper

The files in `data/raw` were extracted during scrapping the TripAdvisor website for attraction reviews.
The reviews extracted are only in Bahasa Indonesia.

## Installation

Install selenium to run code

```bash
pip install selenium
```

## Features

- [x] Extract native Bahasa Indonesia reviews
- [x] Able to loop attractions list from a CSV file
- [ ] Create script for 2nd variation of TripAdvisor's site

## Issues/Bugs

- Script 1 not working as intended (2nd variation)
- Reviews without date on top of it cannot be extracted. (~2-10 reviews missing)

## Solution

- Currently final scrape using DataMiner

# Scrapping Result Journal

The file `TripAdvisorJournal` consists of review scrap count.
