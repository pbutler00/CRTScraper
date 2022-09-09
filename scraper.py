from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas
#config will allow us to access the specified url for which we are #not authorized. Sometimes we may get 403 client error while parsing #the link to download the article.

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
googlenews=GoogleNews(start='05/01/2020',end='05/31/2020')
googlenews.search('Critical Race Theory')
result=googlenews.result()
links = []
for article in result:
        links.append(article['link'])

print(links)

for link in links:
    article = Article(link)
    article.download()
    article.parse()
    print(article.text)