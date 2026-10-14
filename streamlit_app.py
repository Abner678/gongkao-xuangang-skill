import streamlit as st
import requests

st.set_page_config(page_title="公考选岗AI", page_icon="🏛️")
st.title("🏛️ 公考选岗（避坑与捡漏）")
st.caption("考得好不如选得好！我是你的专属选岗顾问。")

# 1. 从 Streamlit Secrets 安全读取你刚刚配置的 API 密钥
API_KEY = st.secrets["TOKENDANCE_API_KEY"]
API_URL = "https://api.tokendance.space/v1/chat/completions" # TokenDance 标准 OpenAI 兼容接口
MODEL_NAME = "deepseek-chat" # 使用你额度支持的模型（如 deepseek-chat 或 deepseek-v4-flash）

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "你好！为了帮你精准匹配国考/省考/选调岗位，我们需要先确认你的基本条件。\n\n**第一步：你的最高学历是？**\nA. 大专\nB. 本科\nC. 硕士\nD. 博士\n\n*(请回复选项字母)*"
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("请回复选项或输入你的情况..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI 正在分析你的选岗策略..."):
            try:
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "system", "content": "你是一个专业的公考选岗AI助手。请通过提问和提供选项的方式收集用户条件（学历、专业、政治面貌、基层年限）。每次只问一个问题，等用户回答后再问下一个。最后匹配岗位时，要提供避坑和捡漏建议。"}
                    ] + st.session_state.messages,
                    "temperature": 0.7
                }
                
                response = requests.post(API_URL, headers=headers, json=payload)
                response.raise_for_status()
                reply = response.json()["choices"][0]["message"]["content"]
                
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                st.error(f"调用失败：{e}")
                st.session_state.messages.append({"role": "assistant", "content": "抱歉，我暂时无法连接模型服务。"})

with st.sidebar:
    st.info("🚧 数据接入中，15号国考岗位发布后将实时更新！")
    st.markdown("---")
    st.markdown("**操作指南：**\n1. 回答几个选择题\n2. AI 帮你筛选匹配岗位\n3. 分析竞争度，避开万人坑")
