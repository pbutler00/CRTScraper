import requests
from newspaper import Article
import nltk
nltk.download('punkt')

url = 'https://www.msnbc.com/rachel-maddow-show/maddowblog/mar-lago-case-doj-appeal-trumps-reaction-matters-rcna46983'
raw_html= requests.get(url)
article = Article('')
article.download(raw_html.content)

article.parse()
# nlp helps find article keywords -- isn't currently working
article.nlp()

#To extract title
print("Article's Title:")
print(article.title)
print("------------------")

print("Article's Keywords:")
print(article.keywords)
print("------------------")

print("Article's Summary:")
print(article.summary)
print("------------------")
# #To extract authors
# print("Article's Author(s):")
# print(article.authors)
# print("------------------")
#
# #To extract text
# print("Article's Text:")
# print(article.text)
# print("------------------")
#
# #To extract date
# print("Article's Publish Date:")
# print(article.publish_date)
# print("------------------")
