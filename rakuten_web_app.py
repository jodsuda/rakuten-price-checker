import streamlit as st
import requests
import pandas as pd
import urllib.parse

# ✅ 楽天APIキー & アフィリエイトID
API_KEY = "1049309157477690132"  # ← ここをあなたの楽天APIキーに変更！
AFFILIATE_ID = "469658c6.99518438.469658c7.a3387bd1"  # ← ここをあなたの楽天アフィリエイトIDに変更！

# ✅ Streamlit の基本設定
st.title("🔍 楽天最安値検索ツール")
st.write("キーワードを入力して、楽天市場内の最安値を検索できます！")

# ✅ ユーザー入力（検索キーワード）
keyword = st.text_input("検索キーワードを入力", value="iPhone")

# ✅ 「検索」ボタン
if st.button("🔍 検索する"):
    # ✅ 楽天APIのURL
    url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId={API_KEY}&keyword={urllib.parse.quote(keyword)}&format=json"
    
    # ✅ APIリクエストを送る
    response = requests.get(url)
    data = response.json()

    # ✅ 商品データを取得
    items = data.get("Items", [])

    # ✅ 必要な情報を抽出
    product_list = []
    for item in items:
        product = item["Item"]

        # ✅ 商品URLをエンコードしてアフィリエイトリンクを作成
        encoded_url = urllib.parse.quote(product["itemUrl"], safe='')
        affiliate_url = f"https://hb.afl.rakuten.co.jp/hgc/{AFFILIATE_ID}/?pc={encoded_url}&m={encoded_url}"

        product_list.append({
            "商品名": product["itemName"],
            "価格": f"{product['itemPrice']} 円",
            "ショップ": product["shopName"],
            "アフィリエイトリンク": f"[楽天で見る]({affiliate_url})"
        })

    # ✅ DataFrame に変換 & 表示
    df = pd.DataFrame(product_list)
    
    # ✅ 結果を表として表示
    st.write("### 🏷 検索結果（最安値順）")
    st.dataframe(df, width=700)

    # ✅ CSVダウンロードボタン
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="💾 検索結果をCSVでダウンロード",
        data=csv,
        file_name="rakuten_price_data.csv",
        mime="text/csv"
    )
