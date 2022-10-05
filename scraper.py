from pygooglenews import GoogleNews
from newspaper import Article
from newspaper import Config
import requests
from scrapingbee import ScrapingBeeClient
import nltk
import pandas as pd
import re
import datetime

cnn_date_re = r"[0-9]{4}\/[0-9]{2}\/[0-9]{2}"
our_api_key = "O8IZ2YUTDJ0TK9YV2LY7EAFMM0TB9ID6PGPVZOYA7JIGK33RILWEG28T2VRNBCVRVTV3499R9Z1OZ580"
gn = GoogleNews()
client = ScrapingBeeClient(api_key=our_api_key)

def search(site, date):
    delta = datetime.timedelta(days=1)
    articles = gn.search('Critical Race Theory site:' + site + ' before: ' + (date+delta).strftime('%Y-%m-%d') + ' after: ' + date.strftime('%Y-%m-%d'))
     
    return articles


def add_to_df(df, links, date):
    print("adding to df")
    for link in links:
        raw_html = client.get(link["link"])
        article = Article('')
        article.download(raw_html.content)
        article.parse()
        article.nlp()

        title = authors = fdate = text = summary = keywords = url = source = 'None'

        if article.title:
            title = article.title
        if article.authors:
            authors = article.authors
        if article.text:
            text = article.text
        if article.summary:
            summary = article.summary
        if article.keywords:
            keywords = article.keywords

        fdate = date.strftime('%m-%d-%Y')
        source_re = r"www.\w*.com"
        match = re.search(source_re, link["link"])
        source = match.group()

        df = df.append({'Title':title,'Author':authors,'Date':fdate,'Text':text,'Summary':summary,'Keywords':keywords,'URL':link["link"],'Source':source}, ignore_index = True)
    return df

def main():

    news_data = pd.DataFrame(columns=['Title','Author','Date','Text','Summary','Keywords','URL','Source'])

    sites = ['washingtonpost.com', 'msnbc.com', 'cnn.com', 'nytimes.com', 'foxnews.com']

    database = pd.ExcelWriter('news-data-excel.xlsx')

    start_date = datetime.date(2022,8,24)
    end_date = datetime.date(2022,9,1)
    date_list = pd.date_range(start_date, end_date).tolist()

    for date in date_list[:-1]:
        for site in sites:
            print(site, date.strftime('%m-%d-%Y'))
            new_articles = search(site, date)
            print("next step")
            news_data = add_to_df(news_data, new_articles["entries"], date)

            news_data.to_excel(database)
            database.save()

if __name__ == "__main__":
    main()
