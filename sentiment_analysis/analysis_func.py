import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
# Standard plotly imports
from chart_studio.plotly import plot, iplot as py
import plotly.graph_objects as go
from plotly.offline import iplot, init_notebook_mode
# Using plotly + cufflinks in offline mode
import cufflinks
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)
cufflinks.set_config_file(theme='space')
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"

def filter_df(filepath, attraction, export=None):
  # available attractions: uss, adventure_cove, beach_waterfront, cable_car, sea_aquarium, skyline_luge, wings_of_time
  df = pd.read_excel(filepath)
  mask = (df['attraction'] == attraction)
  dfn = df[mask]
  if export == 'Y':
    dfn.to_excel(f"output/filtered_attractions/{attraction}_data.xlsx", index=False)
  return dfn

def save_excel_sheet(df, filepath, sheetname, index=False):
    # Create file if it does not exist
    if not os.path.exists(filepath):
        df.to_excel(filepath, sheet_name=sheetname, index=index)

    # Otherwise, add a sheet. Overwrite if there exists one with the same name.
    else:
        with pd.ExcelWriter(filepath, engine='openpyxl', if_sheet_exists='replace', mode='a') as writer:
            df.to_excel(writer, sheet_name=sheetname, index=index)


# Word Cloud   
def grab_review_text(dataframe):
    '''
    Combine review text
    '''
    text = " ".join(i for i in dataframe.new_reviews)
    return text
    
def show_wordcloud(dataframe, attraction, text):
    '''
    Generate word cloud with color function
    ===
    output - Figure output name
    '''
    img_mask = np.array(Image.open('singaporemask.jpg'))
    
    def one_color_func(word=None, font_size=None, position=None, 
                   orientation=None, font_path=None, random_state=None):
        h = 36 # 0 - 360
        s = 100 # 0 - 100
        l = 50
        # l = random_state.randint(30, 70) # 0 - 100
        return "hsl({}, {}%, {}%)".format(h, s, l)

    wordcloud = WordCloud(
        width=img_mask.shape[1], 
        height=img_mask.shape[0],
        colormap='Pastel1',
        mask=img_mask,
        color_func=one_color_func,
        background_color='white',
    ).generate(str(text))

    fig = plt.figure(1, figsize=(16, 12))
    plt.axis('off')

    plt.imshow(wordcloud)
    plt.savefig(f'output/figures/{attraction}_wordcloud.png', bbox_inches='tight')
    plt.show()


# Top words overall
def show_topwords_visual(dataframe, attraction):
    fig = px.histogram(dataframe[:15], x='word', y='frequency',
                  title=f"{attraction}: Top 15 Word Distribution")
    fig.show()
    
def top_words(dataframe, attraction, sheet_name):
    text = grab_review_text(dataframe)
    top_words = WordCloud().process_text(text)
    top_words = pd.DataFrame(top_words.items(), columns=['word', 'frequency']).sort_values(by=['frequency'], ascending=False)
    top_words.to_excel(f"output/{attraction}_topwords.xlsx", sheet_name=sheet_name, index=False)
    # print(top_words.head(15))
    show_topwords_visual(top_words, attraction)
 
    
# Sentiment Share Donut Chart
def show_sentiment_share(dataframe, attraction):
    sent_lbl = dataframe['sentiment'].value_counts()
    sent_fig = go.Figure(data=[go.Pie(labels=['positive', 'neutral', 'negative'], values=sent_lbl, hole=.3)])
    sent_fig.update_layout(
        title=f"{attraction}: Sentiment Share",
        legend_title="Sentiment",)
    sent_fig.show()
  
def show_sentvsrating(dataframe, attraction):
    fig = px.histogram(dataframe, x='rating', color='sentiment', barmode='group', 
                       title=f"{attraction}: Ratings vs Sentiment")
    fig.show()
    
def show_attraction_dist(dataframe, attraction):
    fig = px.histogram(dataframe['attraction'], x='attraction', 
                        title=f"{attraction}: Attraction Distribution")
    fig.show()
    
def show_source_dist(dataframe, attraction):
    fig = px.histogram(dataframe['source'], x='source', 
                        title=f"{attraction}: Source Distribution")
    fig.show()
    
def show_rating_dist(dataframe, attraction):
    fig = px.histogram(dataframe['rating'], x='rating', 
                        title=f"{attraction}: Rating Distribution")
    fig.show()
    
def show_revlen_dist(dataframe, attraction):
    fig = px.histogram(dataframe['review_len'], x='review_len', 
                        title=f"{attraction}: Review Text Length Distribution")
    fig.show()
    
def revlen_rating_box(dataframe, attraction):
    fig = px.box(dataframe, x="rating", y="review_len",
                 title=f"{attraction}: Review length vs Ratings Boxplot")
    fig.show()
    
def revlen_sentiment_box(dataframe, attraction):
    fig = px.box(dataframe, x="sentiment", y="review_len",
                 title=f"{attraction}: Review length vs Sentiment Boxplot")
    fig.show()
    
def show_wordcount_dist(dataframe, attraction):
    fig = px.histogram(dataframe['word_count'], x='word_count', 
                        title=f"{attraction}: Word Count Distribution")
    fig.show()
    
def wordcount_revlen(dataframe, attraction):
    fig = px.scatter(dataframe, x='review_len', y='word_count',
                     title=f"{attraction}: Word Count vs Review Length Scatterplot")
    fig.show()
    
def date_sentiment(dataframe, attraction):
    df_t = dataframe.groupby(['date', 'sentiment']).size().reset_index()
    df_t['percentage'] = dataframe.groupby(['date', 'sentiment']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
    df_t.columns = ['date', 'sentiment', 'Counts', 'Percentage']

    fig = px.bar(df_t, 
                 x='date', y=['Counts'], color='sentiment', 
                 color_discrete_map={
                    'positive': 'green',
                    'neutral': 'orange',
                    'negative': 'red'
                                    },
                 text=df_t['Percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), 
                 title=f"{attraction}: Sentiment Percentage Over Time")
    fig.show()

    
### Combined Figures

# Overall
def show_eda(dataframe, attraction):
    show_attraction_dist(dataframe, attraction)
    show_source_dist(dataframe, attraction)
    show_sentiment_share(dataframe, attraction)
    show_revlen_dist(dataframe, attraction)
    show_wordcount_dist(dataframe, attraction)
    wordcount_revlen(dataframe, attraction)
    show_rating_dist(dataframe, attraction)
    revlen_rating_box(dataframe, attraction)
    revlen_sentiment_box(dataframe, attraction)
    date_sentiment(dataframe, attraction)
    
# Specific Attraction
def show_visual(dataframe, attraction):
    
    # Figures
    show_source_dist(dataframe, attraction)
    show_sentiment_share(dataframe, attraction)
    show_sentvsrating(dataframe, attraction)
    show_rating_dist(dataframe, attraction)
    date_sentiment(dataframe, attraction)
    
    # Overall wordcloud
    print(f'\n{attraction} Word Cloud')
    text = grab_review_text(dataframe)
    show_wordcloud(dataframe, attraction, text)
    
    # Top words from attraction
    print(f'\n{attraction} Top 15 Words Overall')
    top_words(dataframe, attraction, "Overall")
    
    # Positive sentiment wordcloud and top words
    pos_mask = (dataframe['sentiment'] == 'positive')
    pos_df = dataframe[pos_mask]
    pos_text = grab_review_text(pos_df)
    print(f'\n{attraction} Positive Wordcloud')
    show_wordcloud(pos_text, f"{attraction} Positive", pos_text)
    print(f'\n{attraction} Top 15 Positive Words')
    top_words(pos_df, attraction, "Positive")
    
    # Neutral sentiment wordcloud and top words
    neu_mask = (dataframe['sentiment'] == 'neutral')
    neu_df = dataframe[neu_mask]
    neu_text = grab_review_text(neu_df)
    print(f'\n{attraction} Neutral Wordcloud')
    show_wordcloud(neu_text, f"{attraction} Neutral", neu_text)
    print(f'\n{attraction} Top 15 Neutral Words')
    top_words(neu_df, attraction, "Neutral")
    
    # Negative sentiment wordcloud and top words
    neg_mask = (dataframe['sentiment'] == 'negative')
    neg_df = dataframe[neg_mask]
    neg_text = grab_review_text(neg_df)
    print(f'\n{attraction} Negative Wordcloud')
    show_wordcloud(neg_text, f"{attraction} Negative", neg_text)
    print(f'\n{attraction} Top 15 Negative Words')
    top_words(neg_df, attraction, "Negative")
    
    # Export high ratings with neutral and negative sentiment
    highrat_negative = dataframe.loc[(dataframe['rating']>=7) & (dataframe['sentiment']=='negative')]
    highrat_neutral = dataframe.loc[(dataframe['rating']>=7) & (dataframe['sentiment']=='neutral')]
    save_excel_sheet(highrat_negative, f"output/{attraction}_highrating_neg_neu.xlsx", 'negative')
    save_excel_sheet(highrat_neutral, f"output/{attraction}_highrating_neg_neu.xlsx", 'neutral')
    