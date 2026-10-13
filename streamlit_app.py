import streamlit as st

# 页面配置
st.set_page_config(page_title="公考选岗AI", page_icon="🏛️")
st.title("🏛️ 公考选岗（避坑与捡漏）")
st.caption("考得好不如选得好！我是你的专属选岗顾问。")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "你好！为了帮你精准匹配国考/省考/选调岗位，我们需要先确认你的基本条件。\n\n**第一步：你的最高学历是？**\nA. 大专\nB. 本科\nC. 硕士\nD. 博士\n\n*(请回复选项字母)*"
        }
    ]

# 渲染历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 接收用户输入
if prompt := st.chat_input("请回复选项或输入你的情况..."):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # AI 回复逻辑
    with st.chat_message("assistant"):
        # ⚠️ 这里目前是模拟回复，15号接入 TokenPay 后替换为真实 API 调用
        # 你也可以现在写死一些逻辑，比如判断用户输入的是A/B/C/D
        reply = "收到！接下来请告诉我你的**专业类别**（例如：计算机类、法学类、经济学类...）"
        
        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# 侧边栏提示
with st.sidebar:
    st.info("🚧 数据接入中，15号国考岗位发布后将实时更新！")
    st.markdown("---")
    st.markdown("**操作指南：**\n1. 回答几个选择题\n2. AI 帮你筛选匹配岗位\n3. 分析竞争度，避开万人坑")
    st.markdown("---")
    st.markdown("**开发者：** 欢迎体验")
