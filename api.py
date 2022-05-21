import requests
import pandas as pd
import numpy as np
import streamlit as st

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
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?"
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
    result = requests.get(url, params)

    # jsonにデコードする
    json_result = result.json()

    # 出力パラメータ―を指定
    item_key = [
        'itemName',
        'mediumImageUrls',
        'itemUrl',
        'reviewAverage',
        'reviewCount']

    item_list = []
    for i in range(0, len(json_result['Items'])):
        tmp_item = {}
        item = json_result['Items'][i]['Item']
        for key, value in item.items():
            if key in item_key:
                tmp_item[key] = value
        item_list.append(tmp_item.copy())

    # データフレームの表示の省略化を無効化
    pd.set_option('display.max_colwidth', 1000)

    # データフレームを作成
    items_df = pd.DataFrame(item_list)

    # 列の順番を入れ替える
    items_df = items_df.reindex(
        columns=[
            'itemName',
            'mediumImageUrls',
            'itemUrl',
            'reviewAverage',
            'reviewCount'])

    # 列名と行番号を変更する:列名は日本語に、行番号は1からの連番にする
    items_df.columns = ['商品名', '商品画像URL', '商品URL', 'レビュー', 'レビュー件数']
    items_df.index = np.arange(1, len(items_df) + 1)

    imageurl = []
    for i in range(1, len(items_df) + 1):
        f_1 = items_df.loc[i, ['商品画像URL']]
        f_2 = f_1.values.tolist()
        f_3 = f_2[0][0]
        f_4 = f_3['imageUrl']
        f_5 = f_4.replace('?_ex=128x128', '')
        imageurl.append(f_5)

    itemname = items_df.loc[:, ['商品名']]
    itemurl = items_df.loc[:, ['商品URL']]
    review = items_df.loc[:, ['レビュー']]
    reviewcount = items_df.loc[:, ['レビュー件数']]

    return(itemname, imageurl, itemurl, review, reviewcount)
