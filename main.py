from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

url = "https://news.ycombinator.com/"
SERVER = 'localhost'
PORT = 27017


def getHTMLdocument(url):
    response = requests.get(url)    
    return response.text

htmlDoc = getHTMLdocument(url)
soup = BeautifulSoup(htmlDoc, 'html.parser')
collection1 = []
collection2 = []
for news in soup.find_all('tr', {"class": "athing"}):
    titleBlock = news.find('a', {"class": "storylink"})
    collection1.append({
        "title": titleBlock.text,
        "url": titleBlock.get("href")
    })   

    if(news.find_next('tr').find('span', {"class": "score"})):               # Checking for valid vote
        vote=news.find_next('tr').find('span', {"class": "score"}).text
    else:
        vote=None

    if(news.find_next('tr').find('a', {"class": "hnuser"})):                 # Checking for valid author
        author=news.find_next('tr').find('a', {"class": "hnuser"}).text
    else:
        author=None
    
    if(news.find_next('tr').find('span', {"class": "age"})):                 # Checking for valid age
        age=news.find_next('tr').find('span', {"class": "age"}).find('a').text
    else:
        age=None


    collection2.append({
        "url": titleBlock.get("href"),
        "meta": {
            "votes": vote,
            "author": author,
            "age": age,
        }
    })      

print("===========Collection1===============")               
print(collection1)
print()
print("===========Collection2===============")
print(collection2)

client = MongoClient(SERVER, PORT)

articles = client['articles']
articles1 = articles['articles1'] # Collection1
articles2 = articles['articles2'] # Collection2

# articles1.delete_many({})
# articles2.delete_many({})
# articles1.insert_many(collection1)
# articles2.insert_many(collection2)

for i in collection1:
    if(articles1.count_documents({'url': i['url']})<1):
        articles1.insert_one(i)

for i in collection2:
    if(articles2.count_documents({'url': i['url']})<1):
        articles2.insert_one(i)