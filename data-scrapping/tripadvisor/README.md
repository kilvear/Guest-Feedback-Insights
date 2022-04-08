
# TripAdvisor Scrapper

The files in `data/raw` were extracted during scrapping the TripAdvisor website for attraction reviews.
The reviews extracted are only in Bahasa Indonesia.

## Installation

Install selenium to run code

```bash
pip install selenium
```

## Features

- [x]  Extract native Bahasa Indonesia reviews
- [x]  Able to loop attractions list from a CSV file
- [ ]  Create script for 2nd variation of TripAdvisor's site
- [ ]  Convert ipynb file to proper py file

## Bugs
- TripAdvisor counting some English reviews as native.
- Reviews without date on top of it cannot be extracted.

# Scrapping Result Journal (Incomplete)

- Based on STB Trade Show 2018 - Flyer (Indonesia Market)
- Only links compatible with current script

| Last Scrapped | Attraction                       | Zone                 | Link                                                                                                                          | Total Reviews | Reviews Scrapped |
| ------------- | -------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------- | ---------------- |
| 2022-08-04    | iFly Singapore                   | Beaches              | https://www.tripadvisor.co.id/Attraction_Review-g294264-d2180413-Reviews-IFly_Singapore-Sentosa_Island.html                   | 678           |       2           |
| 2022-08-04    | Wave House Sentosa               | Beaches              | https://www.tripadvisor.co.id/Attraction_Review-g294264-d2005250-Reviews-Wave_House_Sentosa-Sentosa_Island.html               | 222           |       1           |
| 2022-08-04    | KidZania Singapore               | Beaches              | https://www.tripadvisor.co.id/Attraction_Review-g294264-d7789437-Reviews-KidZania_Singapore-Sentosa_Island.html               | 561           |        2          |
| 2022-08-04    | Wings of Time                    | Beaches              | https://www.tripadvisor.co.id/Attraction_Review-g294264-d1371247-Reviews-Wings_of_Time-Sentosa_Island.html                    | 2124          |        59          |
| 2022-08-04    | Tiger Sky Tower                  | Imbiah Lookout       | https://www.tripadvisor.co.id/Attraction_Review-g294264-d1892452-Reviews-Tiger_Sky_Tower-Sentosa_Island.html                  | 546           |        14          |
| 2022-08-04    | Sentosa 4D AdventureLand         | Imbiah Lookout       | https://www.tripadvisor.co.id/Attraction_Review-g294264-d1936430-Reviews-Sentosa_4D_Adventureland-Sentosa_Island.html         | 478           |      1            |
| 2022-08-04    | Madame Tussauds                  | Imbiah Lookout       | https://www.tripadvisor.co.id/Attraction_Review-g294264-d7178019-Reviews-Madame_Tussauds_Singapore-Sentosa_Island.html        | 2103          |      108            |
| 2022-08-04    | Butterfly Park & Insect Kingdom  | Imbiah Lookout       | https://www.tripadvisor.co.id/Attraction_Review-g294264-d338375-Reviews-Butterfly_Park_Insect_Kingdom-Sentosa_Island.html     | 604           |      3            |
| 2022-08-04    | Adventure Cove Waterpark         | Resort World Sentosa | https://www.tripadvisor.co.id/Attraction_Review-g294264-d3747640-Reviews-Adventure_Cove_Waterpark-Sentosa_Island.html         | 2480          |        15          |
| 2022-08-04    | S.E.A Aquarium                   | Resort World Sentosa | https://www.tripadvisor.co.id/Attraction_Review-g294264-d4009739-Reviews-S_E_A_Aquarium-Sentosa_Island.html                   | 6745          | 141              |
| 2022-08-04    | The Maritime Experiential Museum | Resort World Sentosa | https://www.tripadvisor.co.id/Attraction_Review-g294264-d1450601-Reviews-The_Maritime_Experiential_Museum-Sentosa_Island.html | 305           |      10            |
