import requests
import streamlit as st
from transmit import SearchResult

"""
long : minprice
long : maxprice
string : genreid
bool   : asurakuflag
string : asurakuarea  （県名を～県で）エラー吐くので一旦停止中
string : genreid
"""


def search_product(search_options):
    # 楽天商品検索APIリクエストURL
    image_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?"
    # 入力パラメーターを指定

    # 開発用に追加、プルリク時に削除必須
    with open("./secret.txt", "r") as f:
        app_id = int(f.read())

    params = {
        "applicationId": app_id,  # st.secret.AppID
        "keyword": "おもしろ雑貨",
        "format": "json",
        "imageFlag": 1,
        "minPrice": search_options.minPrice,
        "maxPrice": search_options.maxPrice,
        "genreId": search_options.genreId,
        "asurakuFlag": search_options.asurakuFlag,
    }
    if search_options.asurakuFlag is True:
        params["asurakuArea"] = search_options.asurakuArea

    # APIを実行して結果を取得する
    result = requests.get(image_url, params)

    # jsonにデコードする
    json_result = result.json()
    return reshape_result(json_result)


def reshape_result(json_result):
    item_list = []
    for i in range(0, len(json_result["Items"])):
        item = json_result["Items"][i]["Item"]  # これが一つの商品データ
        item_name = item["itemName"]
        item_url = item["itemUrl"]
        image_urls = item["mediumImageUrls"]
        image_url = image_urls[0]["imageUrl"].replace("?_ex=128x128", "")
        review = item["reviewAverage"]
        n_review = item["reviewCount"]
        search_result = SearchResult(
            item_name, item_url, image_url, review, n_review)
        item_list.append(search_result)
    return item_list
