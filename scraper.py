from newspaper import Article
from newspaper import Config
import requests
from scrapingbee import ScrapingBeeClient
import nltk
import pandas as pd
nltk.download('punkt')

our_api_key = "O8IZ2YUTDJ0TK9YV2LY7EAFMM0TB9ID6PGPVZOYA7JIGK33RILWEG28T2VRNBCVRVTV3499R9Z1OZ580"
gn = GoogleNews()
client = ScrapingBeeClient(api_key=our_api_key)

news_data = pd.Dataframe(columns=['Title','Author','Date','Text','Summary','Keywords'])

wapo = gn.search('Critical Race Theory site:washingtonpost.com before:'+start_day'after:'+end_day)
msnbc = gn.search('Critical Race Theory site:msnbc.com before:'+start_day'after:'+end_day)
cnn = gn.search('Critical Race Theory site:cnn.com before:'+start_day'after:'+end_day)
nyt = gn.search('Critical Race Theory site:nytimes.com before:'+start_day'after:'+end_day)
fox = gn.search('Critical Race Theory site:foxnews.com before:'+start_day'after:'+end_day)

def add_to_df(df, links):
    for link in links:
        raw_html = client.get(link["link"])
        article = Article('')
        article.download(raw_html.content)
        article.parse()
        article.nlp()

        if article.title:
            title = article.title
        else:
            title = 'None'
        if article.authors:
            authors = article.authors
        else:
            authors = 'None'
        if article.publish_date:
            date = article.publish_date
        else:
            date = 'None'
        if article.text:
            text = article.text
        else:
            text = 'None'
        if article.summary:
            summary = article.summary
        else:
            summary = 'None'
        if article.keywords:
            keywords = article.keywords
        else:
            keywords = 'None'

        df = df.append({'Title':title,'Author':author,'Date':date,'Text':text,'Summary':summary,'Keywords':keywords})
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
