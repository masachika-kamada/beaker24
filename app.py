import streamlit as st
import api


def sidebar():
    # 検索条件設定
    st.sidebar.write("""
    # プレゼント設定
    プレゼントを贈る相手に喜んでもらえるように、条件を絞りましょう。
    """)

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
            ('希望', '指定なし')
        )
        if asurakuflag == '希望':
            asurakuarea = st.selectbox(
                "配送先の都道府県を選んでください",
                ('北海道',
                 '青森県',
                 '岩手県',
                 '宮城県',
                 '秋田県',
                 '山形県',
                 '福島県',
                 '茨城県',
                 '栃木県',
                 '群馬県',
                 '埼玉県',
                 '千葉県',
                 '東京都',
                 '神奈川県',
                 '新潟県',
                 '富山県',
                 '石川県',
                 '福井県',
                 '山梨県',
                 '長野県',
                 '岐阜県',
                 '静岡県',
                 '愛知県',
                 '三重県',
                 '滋賀県',
                 '京都府',
                 '大阪府',
                 '兵庫県',
                 '奈良県',
                 '和歌山県',
                 '鳥取県',
                 '島根県',
                 '岡山県',
                 '広島県',
                 '山口県',
                 '徳島県',
                 '香川県',
                 '愛媛県',
                 '高知県',
                 '福岡県',
                 '佐賀県',
                 '長崎県',
                 '熊本県',
                 '大分県',
                 '宮崎県',
                 '鹿児島県',
                 '沖縄県'))
        else:
            asurakuarea = None

    search_button = st.sidebar.button("検索")
    if search_button:
        return budget, category, asurakuflag, asurakuarea


def main():
    st.title("誕生日プレゼントガチャ")

    ret = sidebar()
    prefectures = {
        '北海道': 1,
        '青森県': 2,
        '岩手県': 3,
        '宮城県': 4,
        '秋田県': 5,
        '山形県': 6,
        '福島県': 7,
        '茨城県': 8,
        '栃木県': 9,
        '群馬県': 10,
        '埼玉県': 11,
        '千葉県': 12,
        '東京都': 13,
        '神奈川県': 14,
        '新潟県': 15,
        '富山県': 16,
        '石川県': 17,
        '福井県': 18,
        '山梨県': 19,
        '長野県': 20,
        '岐阜県': 21,
        '静岡県': 22,
        '愛知県': 23,
        '三重県': 24,
        '滋賀県': 25,
        '京都府': 26,
        '大阪府': 27,
        '兵庫県': 28,
        '奈良県': 29,
        '和歌山県': 30,
        '鳥取県': 31,
        '島根県': 32,
        '岡山県': 33,
        '広島県': 34,
        '山口県': 35,
        '徳島県': 36,
        '香川県': 37,
        '愛媛県': 38,
        '高知県': 39,
        '福岡県': 40,
        '佐賀県': 41,
        '長崎県': 42,
        '熊本県': 43,
        '大分県': 44,
        '宮崎県': 45,
        '鹿児島県': 46,
        '沖縄県': 47}

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
