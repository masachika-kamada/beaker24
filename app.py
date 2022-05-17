import streamlit as st


def sidebar():
    # 検索条件設定
    st.sidebar.write("""
    # プレゼント設定
    プレゼントを贈る相手に喜んでもらえるように、条件を絞りましょう。
    """)

    # セレクトボックスとラジオボタン、処理は同じだけどどっちが見やすい？
    target = st.sidebar.selectbox(
        "誰に贈りますか？",
        ("家族", "友人", "恋人")
    )

    with st.sidebar:
        sex = st.radio(
            "贈り相手の性別",
            ("男性", "女性", "その他")
        )

    search_button = st.sidebar.button("検索")
    if search_button:
        return target, sex


def main():
    st.title("誕生日プレゼントガチャ")

    ret = sidebar()

    if ret is not None:
        data = ["かばん, 1kg, 1000円", "靴, 500g, 7000円"]
        for i in range(len(data)):
            expander = st.expander(f"プレゼント候補{i + 1}の詳細")
            expander.write(data[i])


if __name__ == "__main__":
    main()
