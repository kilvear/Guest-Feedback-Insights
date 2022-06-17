from transformers import pipeline
import sentencepiece
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="sdcsentiment-584f24f06d91.json"
from google.cloud import language_v1

client = language_v1.LanguageServiceClient()

def get_sentiment_hf(text, modelname):
    '''
    === Info ===
    Returns label for sentiment model
    '''
    sentiment_model = pipeline(
                                'sentiment-analysis',
                                model=modelname,
                                tokenizer=modelname
                              )
    prediction = sentiment_model(text)[0]['label']
    return prediction.lower()

def get_sentiment_gcp(text):
  document = language_v1.Document(
    content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language='id'
)
  sentiment = client.analyze_sentiment(
    request={"document": document}
).document_sentiment
  
  if sentiment.score >= 0.5:
    output = 'positive'
  elif sentiment.score >= 0:
    output = 'neutral'
  else:
    output = 'negative'
  return output