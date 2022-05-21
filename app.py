import streamlit as st
import api
import json


def sidebar():
    # 検索条件設定
    st.sidebar.write("""
    # プレゼント設定
    プレゼントを贈る相手に喜んでもらえるように、条件を絞りましょう。
    """)

    # 都道府県データの読み込み
    with open("./prefectures.json", mode="r", encoding="utf-8") as f:
        raw = f.read()
        prefec = json.loads(raw)

    with st.sidebar:
        budget = st.radio(
            "プレゼントの予算",
            ("1000~3000円", "3000~5000円", "5000~7000円", "7000~1万円", "1万円以上")
        )
        category = st.radio(
            "カテゴリ",
            ("レディースファッション", "メンズファッション", "日用品雑貨・文房具・手芸")  # 追加必要
        )
        asurakuflag = st.radio(
            '翌日配送',
            ('指定なし', '希望')
        )
        if asurakuflag == '希望':
            asurakuarea = st.selectbox(
                "配送先の都道府県を選んでください",
                prefec.keys())
        else:
            asurakuarea = None

    search_button = st.sidebar.button("検索")
    if search_button:
        return budget, category, asurakuflag, asurakuarea


def main():
    st.title("誕生日プレゼントガチャ")

    ret = sidebar()

    if ret is not None:
        # プレゼントの予算
        Search_info = []
        if(ret[0] == "1000~3000円"):
            Search_info.append(1000)
            Search_info.append(3000)
        elif(ret[0] == "3000~5000円"):
            Search_info.append(3000)
            Search_info.append(5000)
        elif(ret[0] == "5000~7000円"):
            Search_info.append(5000)
            Search_info.append(7000)
        elif(ret[0] == "7000~1万円"):
            Search_info.append(7000)
            Search_info.append(10000)
        elif(ret[0] == "1万円以上"):
            Search_info.append(10000)
            Search_info.append(999999999)

        if(ret[1] == "レディースファッション"):
            Search_info.append(100371)
        elif(ret[1] == "メンズファッション"):
            Search_info.append(551177)
        elif(ret[1] == "日用品雑貨・文房具・手芸"):
            Search_info.append(215783)

        if(ret[2] == '希望'):
            Search_info.append(1)
        elif(ret[2] == '指定なし'):
            Search_info.append(0)

        if(ret[3] is None):
            Search_info.append(0)
        else:
            Search_info.append(prefectures[ret[3]])

        Search_info.append(ret[1])
        # Search_info.append(ret[2])
        print(Search_info[0], Search_info[1], Search_info[2])

        # api.pyで検索
        itemname, imageurl, itemurl, review, reviewcount = api.api(
            Search_info[0], Search_info[1], Search_info[2], Search_info[3], Search_info[4])

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
