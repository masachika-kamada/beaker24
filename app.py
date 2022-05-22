import streamlit as st
import json
from api import search_product
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

    # カテゴリデータの読み込み
    with open("./categories.json", mode="r", encoding="utf-8") as f:
        raw = f.read()
        category_codes = json.loads(raw)

    with st.sidebar:
        budget = st.radio(
            "プレゼントの予算",
            ("1000~3000円", "3000~5000円", "5000~7000円", "7000~1万円", "1万円以上")
        )
        category = st.radio(
            "カテゴリ",
            category_codes.keys()
        )
        category_code = category_codes[category]
        next_day_delivery = st.radio(
            "翌日配送",
            ("指定なし", "希望する")
        )
        if next_day_delivery == "希望する":
            prefec = st.selectbox(
                "配送先の都道府県を選んでください",
                prefec_codes.keys())
            prefec_code = prefec_codes[prefec]
        else:
            prefec_code = None
        wrapping = st.radio(
            "ラッピング",
            ('指定なし', '希望する')
        )

    search_button = st.sidebar.button("検索")
    if search_button:
        search_options.set(budget, category_code, next_day_delivery, prefec_code, wrapping)
        return True


def main():
    st.title("誕生日プレゼントガチャ")

    search_options = SearchOptions()
    ret = sidebar(search_options)

    if ret is not None:
        # api.pyで検索
        items = search_product(search_options)

        if len(items) != 0:
            for i, item in enumerate(items):
                st.image(item.imageUrl, width=400)
                expander = st.expander(f"プレゼント候補 {i + 1} の詳細")
                expander.markdown(f"###### 商品名：{item.itemName}")
                expander.markdown(f"###### レビュー({item.n_review}件)：{item.review}")
                expander.markdown(f"URL：{item.itemUrl}")
                expander.markdown(f"###### 翌日配送：{item.nextDayDelivery}")
                if item.nextDayDelivery == "可":
                    expander.caption("～対象地域～")
                    expander.caption(item.asurakuArea)
        else:
            st.write("お求めの商品はありませんでした。")
    st.image("https://webservice.rakuten.co.jp/img/credit_31130.gif")


if __name__ == "__main__":
    main()
