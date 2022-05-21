import streamlit as st
import api
import json
from transmit import SearchOptions


def sidebar(search_options):
    # 検索条件設定
    st.sidebar.write("""
    # プレゼント設定
    プレゼントを贈る相手に喜んでもらえるように、条件を絞りましょう。
    """)

    # 都道府県データの読み込み
    with open("./prefectures.json", mode="r", encoding="utf-8") as f:
        raw = f.read()
        prefec_codes = json.loads(raw)

    with st.sidebar:
        budget = st.radio(
            "プレゼントの予算",
            ("1000~3000円", "3000~5000円", "5000~7000円", "7000~1万円", "1万円以上")
        )
        category = st.radio(
            "カテゴリ",
            ("レディースファッション", "メンズファッション", "日用品雑貨・文房具・手芸")  # 追加必要
        )
        next_day_delivery = st.radio(
            '翌日配送',
            ('指定なし', '希望')
        )
        if next_day_delivery == '希望':
            prefec = st.selectbox(
                "配送先の都道府県を選んでください",
                prefec_codes.keys())
            prefec_code = prefec_codes[prefec]
        else:
            prefec_code = None

    search_button = st.sidebar.button("検索")
    if search_button:
        search_options.set(budget, category, next_day_delivery, prefec_code)
        return True


def main():
    st.title("誕生日プレゼントガチャ")

    search_options = SearchOptions()
    ret = sidebar(search_options)

    if ret is not None:
        # api.pyで検索
        itemname, imageurl, itemurl, review, reviewcount = api.api(search_options)

        if (len(itemname) != 0):
            # 出力
            for i in range(len(itemname['商品名'])):
                st.image(imageurl[i], width=400)
                expander = st.expander(f"プレゼント候補{i + 1}の詳細")
                expander.markdown('###### 商品：' + itemname['商品名'][i + 1])
                expander.markdown('###### レビュー({}件)：'.format(
                    str(reviewcount['レビュー件数'][i + 1])) + str(review['レビュー'][i + 1]))
                expander.markdown(
                    '商品URL：' + itemurl['商品URL'][i + 1], unsafe_allow_html=True)
        else:
            st.write("お求めの商品はありませんでした。")
    st.image("https://webservice.rakuten.co.jp/img/credit_31130.gif")


if __name__ == "__main__":
    main()
