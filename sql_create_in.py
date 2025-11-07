import streamlit as st

st.set_page_config(layout="wide")  # ワイド画面にする

# タイトル
st.title("IN句生成ツール")

# 2カラムレイアウト
left, right = st.columns([2, 1])

with left:
    # 入力欄
    text_input = st.text_area("ExcelやSQLの出力結果の列から行を貼り付け", height=200)

# チェックボックス（横並び）
cb1, cb2 = st.columns(2)
with cb1:
    use_single_quote = st.checkbox("シングルクォーテーション（'）で括る", value=True)
with cb2:
    newline_every_10 = st.checkbox("10要素ごとに改行", value=True)

# ★ 変換実行ボタン
run_button = st.button("変換する")

result = ""  # 初期値

if run_button:  # ボタン押下時のみ処理
    quote = "'" if use_single_quote else '"'

    # 入力値処理
    values = [v.strip() for v in text_input.splitlines() if v.strip()]

    def chunk_list(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i+n]

    if values:
        if newline_every_10:
            chunks = []
            for chunk in chunk_list(values, 10):
                chunks.append(", ".join(f"{quote}{v}{quote}" for v in chunk))
            formatted_values = ",\n".join(chunks)
        else:
            formatted_values = ", ".join(f"{quote}{v}{quote}" for v in values)

        result = f"IN (\n{formatted_values}\n)"
    else:
        result = ""

# 結果表示
st.subheader("変換結果（コピー用）")
st.code(result, language="sql")

# 右側説明欄
with right:
    st.subheader("ツール説明")
    st.write("""
        エクセルやSQLの出力結果の列をコピーし、  
        ワンアクションでIN句を作成するためのツール。
        """)

    st.subheader("仕様")
    st.write("""
        - 値を**シングルクォーテーション**で囲みます。
        （囲まない場合はチェックを外してください）
        - 値を**10要素ごとに改行**します。
        （改行しない場合はチェックを外してください）
        - **空行は無視**します。
        - **IN句の個数上限**は考慮していません。
        """)
