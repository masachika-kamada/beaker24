import streamlit as st


def sidebar():
    # 検索条件設定
    st.sidebar.write("""
    # プレゼント設定
    プレゼントを贈る相手に喜んでもらえるように、条件を絞りましょう。
    """)

    with st.sidebar:
        target = st.radio(
            "誰に贈りますか？",
            ("家族", "友人", "恋人")
        )
        sex = st.radio(
            "贈り相手の性別",
            ("男性", "女性", "その他")
        )
        old = st.radio(
            "贈り相手の年齢",
            ("0~10歳", "10~20歳", "20~30歳", "30~40歳")
        )
        budget = st.radio(
            "プレゼントの予算",
            ("1000~3000円", "3000~5000円", "5000~7000円", "7000~1万円", "1万円以上")
        )
        category = st.radio(
            "カテゴリ",
            ("", "", "")
        )
        days = st.radio(
            "プレゼントが届くまでの時間",
            ("1日以内", "2", "3", "more")
        )
        star = st.radio(
            "プレゼントのレビュー",
            ("★2以上", "★3以上", "★4以上")
        )

    search_button = st.sidebar.button("検索")
    if search_button:
        return target, sex, old, budget, category, days, star


def main():
    st.title("誕生日プレゼントガチャ")

    ret = sidebar()

    if ret is not None:
        data = [["かばん", "1kg", "1000円",
                 "https://image.rakuten.co.jp/e-smart/cabinet/shohin11/b-to-b-6936.jpg"],
                ["靴", "500g", "7000円",
                 "https://image.rakuten.co.jp/hype/cabinet/sgazo29/7992844_1.jpg"]]
        for i in range(len(data)):
            st.image(data[i][-1], width=400)
            expander = st.expander(f"プレゼント候補{i + 1}の詳細")
            expander.write(data[i][:-1])


if __name__ == "__main__":
    main()
