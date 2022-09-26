from newspaper import Article
from newspaper import Config
import requests
from scrapingbee import ScrapingBeeClient
import nltk
import re
import pandas as pd
nltk.download('punkt')

cnn_date_re = r"[0-9]{4}\/[0-9]{2}\/[0-9]{2}"

our_api_key = "O8IZ2YUTDJ0TK9YV2LY7EAFMM0TB9ID6PGPVZOYA7JIGK33RILWEG28T2VRNBCVRVTV3499R9Z1OZ580"
gn = GoogleNews()
client = ScrapingBeeClient(api_key=our_api_key)

news_data = pd.Dataframe(columns=['Title','Author','Date','Text','Summary','Keywords','URL','Source'])

sites = ['washingtonpost.com', 'msnbc.com', 'cnn.com', 'nytimes.com', 'foxnews.com']

articles = []
for site in sites:
    if site != "cnn.com":
        new_articles = search(site)
        articles += new_articles
    else:
        # do something to correct the CNN sourcing
        new_articles = search(site)
        articles += new_articles


def search(site):
    articles = gn.search('Critical Race Theory site:' + site + ' before:'+start_day+'after:'+end_day)
    return articles


def add_to_df(df, links):
    for link in links:
        raw_html = client.get(link["link"])
        article = Article('')
        article.download(raw_html.content)
        article.parse()
        article.nlp()

        title = authors = date = text = summary = keywords = url = source = 'None'

        if article.title:
            title = article.title
        if article.authors:
            authors = article.authors
        if article.publish_date:
            date = article.publish_date
        if article.text:
            text = article.text
        if article.summary:
            summary = article.summary
        if article.keywords:
            keywords = article.keywords

        df = df.append({'Title':title,'Author':authors,'Date':date,'Text':text,'Summary':summary,'Keywords':keywords,'URL':url,'Source':source)
    return df














































# from GoogleNews import GoogleNews
# from newspaper import Article
# from newspaper import Config
# # import pandas
# import requests
# #config will allow us to access the specified url for which we are #not authorized. Sometimes we may get 403 client error while parsing #the link to download the article.
#
# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# config = Config()
# config.browser_user_agent = user_agent
# googlenews=GoogleNews(start='05/01/2020',end='05/31/2020')
# googlenews.search('Critical Race Theory')
# result=googlenews.result()
# links = []
# for article in result:
#         links.append(article['link'])
#
# print(links)
#
# for link in links:
#     raw_html = requests.get(link)
#     article = Article('')
#     article.download(raw_html.content)
#     article.parse()
#
#     print("Article's Title:")
#     print(article.title)
#     print("------------------")
#
#     print("Article's Text:")
#     print(article.text)
#     print("------------------")
