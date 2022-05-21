import streamlit as st
import api

def sidebar():
    # 検索条件設定
    st.sidebar.write("""
    # プレゼント設定
    プレゼントを贈る相手に喜んでもらえるように、条件を絞りましょう。
    """)

    with st.sidebar:
        # target = st.radio(
        #     "誰に贈りますか？",
        #     ("家族", "友人", "恋人")
        # )
        # sex = st.radio(
        #     "贈り相手の性別",
        #     ("男性", "女性", "その他")
        # )
        # old = st.radio(
        #     "贈り相手の年齢",
        #     ("0~10歳", "10~20歳", "20~30歳", "30~40歳")
        # )
        budget = st.radio(
            "プレゼントの予算",
            ("1000~3000円", "3000~5000円", "5000~7000円", "7000~1万円", "1万円以上")
        )
        category = st.radio(
            "カテゴリ",
            ("", "", "")  # 追加必要
        )
        category = 551177

        # asurakuflag = st.checkbox('翌日配達を望む')
        # if asurakuflag:
        #     asurakuflag = 
        #     asurakufarea = st.selectbox(
        #         "配送先の都道府県を選んでください",
        #         ('北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県')
        #     )
        # else:
        #     asurakuflag = 0
        #     asurakufarea = None
        # days = st.radio(
        #     "プレゼントが届くまでの時間",
        #     ("1日以内", "2", "3", "more")
        # )
        # star = st.radio(
        #     "プレゼントのレビュー",
        #     ("★2以上", "★3以上", "★4以上")
        # )
        # print(days)

    search_button = st.sidebar.button("検索")
    if search_button:
        return budget, category
                                # asurakuflag, asurakufarea

def main():
    st.title("誕生日プレゼントガチャ")

    ret = sidebar()

    if ret is not None:
        #プレゼントの予算
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
        
        Search_info.append(ret[1])
        # Search_info.append(ret[2])
        print(Search_info[0],Search_info[1],Search_info[2])

        #api.pyで検索
        itemname, imageurl, itemurl, review = api.api(Search_info[0],Search_info[1],Search_info[2])

        if (len(itemname) != 0):
            #サンプルデータ
            # data = [["かばん", "1kg", "1000円",
            #          "https://image.rakuten.co.jp/e-smart/cabinet/shohin11/b-to-b-6936.jpg"],
            #         ["靴", "500g", "7000円",
            #          "https://image.rakuten.co.jp/hype/cabinet/sgazo29/7992844_1.jpg"]]
            
            #出力
            for i in range(len(itemname['商品名'])):
                st.image(imageurl[i], width=400)
                expander = st.expander(f"プレゼント候補{i + 1}の詳細")
                expander.markdown('###### 商品：'+ itemname['商品名'][i+1])
                expander.markdown('###### レビュー：'+ str(review['レビュー'][i+1]))
                expander.markdown('商品URL：'+ itemurl['商品URL'][i+1], unsafe_allow_html=True)
        else:
            st.write("お求めの商品はありませんでした。")
    st.image("https://webservice.rakuten.co.jp/img/credit_31130.gif")

if __name__ == "__main__":
    main()
