import numpy as np
import pandas as pd
import ast
import re
import spacy
from emot.emo_unicode import UNICODE_EMOJI, UNICODE_EMOJI_ALIAS, EMOTICONS_EMO
import translators as ts
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from transformers import pipeline

# Indonesian spacy object
id_nlp = spacy.blank('id')
# English spacy object
nlp = spacy.load("en_core_web_lg")

# Custom stopwords
eng_stopwords = set(line.strip() for line in open('../resources/stop_words_english.txt', encoding='utf-8'))
id_stopwords = set(line.strip() for line in open('../resources/stop_words_bahasaindonesia.txt', encoding='utf-8'))
new_stopwords = eng_stopwords.union(id_stopwords)
nlp.Defaults.stop_words |= new_stopwords

# Create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Create summary model
summary_model = pipeline("summarization",
                model="cahya/t5-base-indonesian-summarization-cased",
                tokenizer="cahya/t5-base-indonesian-summarization-cased")


def preprocess_sentiment(df):
  '''
  Preprocessing
  - Lowercasing reviews
  - Translate emojis/emoticons to Bahasa Indonesia
  - Remove punctuation and symbols
  - Remove empty rows
  - Fix slang words
  - Summarize reviews with more than 1536 characters
  - Stemming
  - Remove stop words
  '''
  file = open("../resources/bahasa_indonesia_slangwords.txt", "r")
  contents = file.read()
  slangwords = ast.literal_eval(contents)
  
  def tokenize_id(text):
    text_list = [token.text for i, token in enumerate(id_nlp(text))]
    return text_list
  
  def translate_emoji(text):
    '''
    Tokenizes review using SpaCy Indonesia, replace any emoji with English form and translate it to Indonesian
    '''
    all_emoji_emoticons = {**EMOTICONS_EMO,**UNICODE_EMOJI_ALIAS, **UNICODE_EMOJI_ALIAS}
    all_emoji_emoticons = {k:v.replace(":","").replace("_"," ").strip() for k,v in all_emoji_emoticons.items()}
    
    text_list = tokenize_id(text.replace("  ", ""))
    for index, token in enumerate(text_list):
        for key, value in all_emoji_emoticons.items():
            if key in token:
                text_list[index]=token.replace(key, ts.google(all_emoji_emoticons[key], from_language='en', to_language='id'))
                
    rejoin_text = ' '.join(text_list)
    return rejoin_text
  
  df['new_reviews'] = df['review'].apply(lambda x: " ".join(x.lower() for x in x.split()))
  df['new_reviews'] = df['new_reviews'].apply(lambda x: translate_emoji(x))
  df['new_reviews'] = df['new_reviews'].str.replace('[^\w\s]','',regex=True)
  
  # Remove empty rows
  df[df['new_reviews'].str.strip().astype(bool)]
  
  # Fix slang words
  df['new_reviews'] = df['new_reviews'].apply(lambda x: " ".join(slangwords.get(word, word) for word in tokenize_id(x)))
  
  # Summarize reviews
  # Reviews more than 1536 characters (Average indonesian word has 3 characters times 512 which is max sentiment tensor input)
  mask = (df['new_reviews'].str.len() >= 1536)
  df.loc[mask, 'new_reviews'] = df.loc[mask, 'new_reviews'].apply(lambda x: summary_model(x)[0]['summary_text']).str.replace('[^\w\s]','',regex=True)
  
  # Stemming
  df['new_reviews'] = df['new_reviews'].apply(lambda x: stemmer.stem(x))
  
  # Remove stop words
  df['new_reviews'] = df['new_reviews'].apply(lambda text: 
                                          " ".join(token.text for token in nlp(text) 
                                                   if not token.is_stop))
  
  # Remove empty rows in case review only contain stop words
  df['new_reviews'].replace('', np.nan, inplace=True)
  df.dropna(subset=['new_reviews'], inplace=True)