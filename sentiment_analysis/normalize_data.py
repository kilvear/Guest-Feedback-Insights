import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

def normalize_reviews(filepath):
  '''
  1. Drop duplicated rows
  2. Normalize dates to only the year
  3. Normalize ratings to 10
  '''
  
  df = pd.read_excel(filepath)
  
  # Drop duplicated rows
  df.drop_duplicates(keep='first', inplace=True)
  
  # 1. Normalize dates to only year
  
  # For Google Review dates
  # fix_date_week | fix_date_month | fix_date_year
  # Takes current date and minus off respective day, week, month or year
  def fix_date_day(day):
    date = datetime.datetime.now()
    date = date.date()
    newdate = date - relativedelta(days=day)
    return newdate
  
  def fix_date_week(week):
    date = datetime.datetime.now()
    date = date.date()
    newdate = date - relativedelta(weeks=week)
    return newdate
  
  def fix_date_month(month):
    date = datetime.datetime.now()
    date = date.date()
    newdate = date - relativedelta(months=month)
    return newdate
  
  def fix_date_year(year):
    date = datetime.datetime.now()
    date = date.date()
    newdate = date - relativedelta(years=year)
    return newdate
  
  # Replace date strings with proper year
  # Only up to 10 years
  replace_date = {'sehari lalu': fix_date_day(1),
                  '2 hari lalu': fix_date_day(2),
                  '3 hari lalu': fix_date_day(3),
                  '4 hari lalu': fix_date_day(4),
                  '5 hari lalu': fix_date_day(5),
                  '6 hari lalu': fix_date_day(6),
                  'seminggu lalu': fix_date_week(1),
                  '2 minggu lalu': fix_date_week(2),
                  '3 minggu lalu': fix_date_week(3),
                  '4 minggu lalu': fix_date_week(4),
                  'sebulan lalu': fix_date_month(1),
                  '2 bulan lalu': fix_date_month(2),
                  '3 bulan lalu': fix_date_month(3),
                  '4 bulan lalu': fix_date_month(4),
                  '5 bulan lalu': fix_date_month(5),
                  '6 bulan lalu': fix_date_month(6),
                  '7 bulan lalu': fix_date_month(7),
                  '8 bulan lalu': fix_date_month(8),
                  '9 bulan lalu': fix_date_month(9),
                  '10 bulan lalu': fix_date_month(10),
                  '11 bulan lalu': fix_date_month(11),
                  'setahun lalu': fix_date_year(1),
                  '2 tahun lalu': fix_date_year(2),
                  '3 tahun lalu': fix_date_year(3),
                  '4 tahun lalu': fix_date_year(4),
                  '5 tahun lalu': fix_date_year(5),
                  '6 tahun lalu': fix_date_year(6),
                  '7 tahun lalu': fix_date_year(7),
                  '8 tahun lalu': fix_date_year(8),
                  '9 tahun lalu': fix_date_year(9),
                  '10 tahun lalu': fix_date_year(10),}

  
  # Google review mask
  dfg = df[(df['source']=='google_reviews')].copy()
  dfg = dfg.replace({"date": replace_date})
  dfg['date'] = pd.DatetimeIndex(dfg['date']).year
  
  # Other websites
  # Create mask for non-google rows
  ngmask = (df['source'] != 'google_reviews')

  # Dataframe for non-google rows
  df_ng = df[ngmask]

  # Get proper date rows from non-google df to separate dataframe
  df_ng_prop = df_ng[df_ng['date'].apply(lambda x: isinstance(x, datetime.date))].copy()

  # Extract only year from proper date rows
  df_ng_prop['date'] = pd.DatetimeIndex(df_ng_prop['date']).year

  # Get improper date rows from non-google df to separate dataframe
  df_ng_improp = df_ng[df_ng['date'].apply(lambda x: not isinstance(x, datetime.date))].copy()

  # Convert datatype to string and only extract last 4 index for year
  df_ng_improp['date'] = df_ng_improp['date'].astype(str).str[-4:]

  # Rejoin all dataframes
  df = pd.concat([dfg, df_ng_prop, df_ng_improp], ignore_index=True)
  df['date'] = df['date'].astype(int)
  
  #2. Normalize ratings to 10
  
  # Normalize klook ratings
  replace_rating = {4:8,
                    'Baik': 8,
                    'Sangat Direkomendasikan': 10}
  df[(df['source'] == 'klook')] = df.replace({'rating': replace_rating})
  
  # Normalize TripAdvisor ratings
  ta_mask = (df['source'] == 'tripadvisor')
  # Retrieve index 0 string of rating and multiply by 2
  df.loc[ta_mask, 'rating'] = (df.loc[ta_mask, 'rating'].str[0].astype(int))*2
  
  # Normalize Google Review ratings
    # Mask for Google Review ratings
  g_mask = (df['source'] == 'google_reviews')
  # Retrieve index 14 string of rating and multiply by 2
  df.loc[g_mask, 'rating'] = (df.loc[g_mask, 'rating'].str[14].astype(int))*2
  
  return df