from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# LLMの初期化（APIキーは環境変数かセッションで管理してください）
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# LLMを使って回答を生成する関数
def ask_expert(input_text, expert_type):
    # 専門家の役割をシステムメッセージで設定
    if expert_type == "打撃専門":
        system_msg = "あなたは非常に優秀な野球の打撃コーチです。質問に対して専門的なアドバイスを提供してください。"
    elif expert_type == "守備専門":
        system_msg = "あなたは非常に優秀な野球の守備コーチです。質問に対して専門的なアドバイスを提供してください。"
    else:
        system_msg = "あなたは優秀な野球のコーチです。"

    # プロンプトの作成
    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=input_text)
    ]

    # 回答の取得
    response = llm(messages)
    return response.content

# --- Streamlit UI ---
st.set_page_config(page_title="野球コーチAI", layout="centered")

# タイトルと案内
st.title("⚾ 野球専門コーチAI")
st.markdown("""
最初に「あなたは優秀な野球専門のコーチです。」と表示されます。  
以下の入力欄に質問を記入し、「打撃専門」または「守備専門」のコーチを選んで送信してください。  
選んだ分野に応じて、AIがその専門分野に特化したアドバイスを行います。
""")

# 初期表示のメッセージ
st.info("あなたは優秀な野球専門のコーチです。")

# フォーム入力
with st.form("question_form"):
    input_text = st.text_area("質問を入力してください", placeholder="例: バットのスイングを速くするには？", height=100)
    expert_type = st.radio("どの専門家に相談しますか？", options=["打撃専門", "守備専門"], horizontal=True)
    submitted = st.form_submit_button("送信")

# 回答処理
if submitted:
    if input_text.strip() == "":
        st.warning("質問内容を入力してください。")
    else:
        with st.spinner("AIコーチが回答中..."):
            result = ask_expert(input_text, expert_type)
            st.success("AIコーチの回答:")
            st.write(result)