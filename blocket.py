import requests
from bs4 import BeautifulSoup
from database import check_id_for_blocket, add_id_to_blocket
from telegram_bot import send_blocket_to_telegram

# setup headers
headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-SE,en;q=0.9,sv-SE;q=0.8,sv;q=0.7,en-US;q=0.6',
}


def get_article_data(article):
    # get all data
    time = article.select_one("div > header > time").get_text()
    date = article.select_one("div > header > time").get("datetime")
    url = article.select_one("a").get("href")
    price = article.select_one("div > p").get_text()
    title = article.select_one("div > h1 > a").get_text()
    place = article.select_one("div > header > div").get_text()
    item_id = article.get("id")

    # get img if it exists
    try:
        img = article.select_one("a > img").get("src")

        if not img.endswith(".jpg"):
            img = None
    except:
        img = None

    # get full image
    if img:
        img = img.replace("lithumbs", "images_full")

    # save to dict
    article_dict = {
        "time": time,
        "date": date,
        "url": url,
        "price": price,
        "title": title,
        "place": place,
        "id": item_id,
        "img": img
    }

    return article_dict


def create_params(q, angransade_lan=False, trollhattan=False):

    # create a dictionary of parameters depending on the search variables
    if angransade_lan:
        return {"q": q, "w": 2, "f": "p"}
    elif trollhattan:
        return {"q": q, "w": 1, "f": "p", "m": 208}
    else:
        return {"q": q, "w": 1, "f": "p"}


def blocket(q, al=False, thn=False):
    # create parameters for request
    params = create_params(q, al, thn)

    # make request and save as content
    response = requests.get('https://www.blocket.se/alvsborg',
                            headers=headers,
                            params=params)
    content = response.content

    # scrape for articles and prepare a list
    soup = BeautifulSoup(content, features="lxml")
    articles_soup = soup.find_all("article")  # get articles
    articles = []  # save all articles to a list

    # go through each article and save data
    for article in articles_soup:
        # save only relevant listings
        if len(article) != 5:

            continue
        # get all data
        try:
            article_dict = get_article_data(article)
        except:
            continue

        articles.append(article_dict)

    # check for duplicates and add to server
    for article in articles:

        # skip if already added
        if check_id_for_blocket(article["id"]):
            continue

        # send to telegram
        send_blocket_to_telegram(article)

        # add ID to database so it won't send again
        add_id_to_blocket(article["id"])
