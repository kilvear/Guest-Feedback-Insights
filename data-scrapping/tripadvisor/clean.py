import os
import glob
import pandas as pd
import datetime as dt

def combine_csv(path):
  '''
  Combine all csv files into a single csv
  Example path:
  "c:\\Users\\Luqman\\Desktop\\Guest-Feedback-Insights\\data-scrapping\\tripadvisor\\data\\raw"
  '''
  os.chdir(path)
  extension = 'csv'
  all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
  #combine all files in the list
  combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
  #export to csv
  combined_csv.to_csv( "clean/combined_reviews.csv", index=False, encoding='utf-8-sig')
  
def filter_date(path, year):
  '''
  Filter data from specified year to current 
  Example path:
  "data/raw/combined_reviews.csv"
  '''
  df = pd.read_csv(path)
  # Convert date object to datetime
  df['date'] = pd.to_datetime(df['date'])
  cur_df = df[df['date'].dt.year >= year]
  print(f"Number of rows: {len(cur_df)}")
  cur_df.to_csv(f'data/clean/filtered_{year}plus.csv', index=False)
  