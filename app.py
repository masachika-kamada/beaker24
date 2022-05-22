import streamlit as st
import json
from api import search_product
from transmit import SearchOptions
import streamlit.components.v1 as stc


def sidebar(search_options):
    
        
    # 都道府県データの読み込み
    with open("./prefectures.json", mode="r", encoding="utf-8") as f:
        raw = f.read()
        prefec_codes = json.loads(raw)

    # カテゴリデータの読み込み
    with open("./categories.json", mode="r", encoding="utf-8") as f:
        raw = f.read()
        category_codes = json.loads(raw)

    with st.sidebar:
        stc.html("""
        <head>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Hachi+Maru+Pop&display=swap" rel="stylesheet">  
        </head>
        <div class = "sidebar">      
          <h1>プレゼント設定</h1>
          <p>プレゼントを贈る相手に喜んでもらえるように、条件を絞りましょう。</p>
        </div>
        <style>
          .sidebar{
              font-family: 'Hachi Maru Pop', cursive;
          }
        </style>
        """)

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
    stc.html("""
    <head>
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Hachi+Maru+Pop&display=swap" rel="stylesheet">  
    </head>
    <body>
        <div class = "box14">
          <h1>　　フ<span class =  "char1">ァ</span>ニ<span class = "char2">ー</span>プレゼントアドバイザ<span class = "char3">ー</span></h1>
        </div>

        <div class = "title">
          <div class = "intro">
            <a>ひだりうえのさんかくっぽいやつをおしてねぇ。</a>
            <div class = "rotate">&#9756;</div>
          </div>          
        </div>
    </body>

    <style>
    body{
     font-family: 'Hachi Maru Pop', cursive;
    }
    .char1{
        color:#00CDEA;
    }
    .char2{
        color:#00CDEA;
    }
    .char3{
        color:#00CDEA;
    }
    .rotate{
      position:absolute;
      left:0;
      top:5px;
      font-size:40px;
      color:white;
      transition:5s all;
    }
    a{
        color:black;
    }
    a:hover{
        color:#FFF218;
    }
    a:hover + .rotate{
        color:#00CDEA;
        transform:rotate(405deg);
    }
    
    .title{
        width:75%;
        height:100px;
    }
    .box14{
        width:100%;
        height:50px;
        padding:0em 1em;
        margin: 0 0;
        color: #FF4E63;
        backgroud: #d6ebff;
        border-bottom: solid 6px #FFF218;
        border-radius: 9px;
    }
    .box14 h1{
        margin:0;
        padding:0;
        font-size:40px;   
    }
    </style>
    """
    )
    

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
                expander.markdown(f"###### 値段：{item.itemPrice}円")
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
