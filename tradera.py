import requests
from bs4 import BeautifulSoup
import json
from database import check_id_for_tradera, add_id_to_tradera
from telegram_bot import send_tradera_to_telegram

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


def tradera(q):
    content = requests.get("https://www.tradera.com/search",
                           headers=headers,
                           params={
                               "q": q,
                               "sellerType": "Private"
                           })
    content = content.content

    # scrape for articles and prepare a list
    soup = BeautifulSoup(content, features="lxml")
    data = soup.select_one("#init-data").get_text()

    # get json data
    json_data = json.loads(data)
    items = json_data["discoverResponse"]["items"]

    items_list = scrape_json_data(items)
    items_list = remove_bad_listings(items_list)

    # add to database and blocket
    send_info(items_list)


def scrape_json_data(items):
    # save important info to list
    items_list = []
    for item in items:

        if item["isShopItem"]:
            continue

        bid = item["currentBid"]
        buy = item["buyNowPrice"]
        shipping = f"{item['shippingPrice']} kr" if item[
            "shippingPrice"].isdigit() else item["shippingPrice"]
        img = item["imageUrl"].replace("//", "")
        url = "https://tradera.se" + item["itemUrl"]
        title = item["shortDescription"]
        seller = item["sellerAlias"]
        bids = item["totalBids"]
        item_id = item["itemId"]
        time = item["timeLeft"].replace("<span class='timeleft'>",
                                        "").replace("</span>",
                                                    "").replace("  ",
                                                                " ").strip()

        items_list.append({
            "bid": bid,
            "buy": buy,
            "shipping": shipping,
            "img": img,
            "url": url,
            "title": title,
            "seller": seller,
            "bids": bids,
            "item_id": item_id,
            "time": time,
            "remove": False
        })

    return items_list


def remove_bad_listings(items_list):
    # remove bad listings
    for item in items_list:
        list_id = item["item_id"]
        title = item["title"]
        seller = item["seller"]

        for checking_item in items_list:

            # skip if same ID
            if list_id == checking_item["item_id"]:
                continue

            if title == checking_item["title"]:
                items_list.remove(checking_item)
                item["remove"] = True
                break

            if seller == checking_item["seller"]:
                items_list.remove(checking_item)
                item["remove"] = True
                break

        if item["remove"]:
            items_list.remove(item)

    return items_list


def send_info(items_list):
    # add to database and blocket
    for item in items_list:

        # skip if already added
        if check_id_for_tradera(item["item_id"]):
            continue

        # send to telegram
        send_tradera_to_telegram(item)

        # add ID to database so it won't send again
        add_id_to_tradera(item["item_id"])
