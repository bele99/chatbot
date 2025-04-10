# AI 八字网页版 MVP 原型 - 使用 Streamlit

import streamlit as st
import datetime
import openai

from lunarcalendar import Converter, ChineseDate

def get_bazi_info(birth_date, birth_time, birth_place, gender):
    from datetime import datetime as dt

    user_datetime = dt.combine(birth_date, birth_time)

    # 使用 lunarcalendar 计算农历
    lunar_date = Converter().solar_to_lunar(user_datetime.year, user_datetime.month, user_datetime.day)
    lunar_year, lunar_month, lunar_day = lunar_date.year, lunar_date.month, lunar_date.day
    is_leap = lunar_date.is_leap_month

    # 返回模拟排盘结果（此处可接专业农历库做真实排盘）
    bazi_info = {
        "阳历": user_datetime.strftime("%Y-%m-%d %H:%M"),
        "农历": f"{lunar_year}年{lunar_month}月{lunar_day}日{'(闰)' if is_leap else ''}",
        "出生地": birth_place,
        "性别": gender,
        "八字四柱": {
            "年柱": "壬子",
            "月柱": "乙卯",
            "日柱": "丙辰",
            "时柱": "庚午"
        },
        "五行比例": {
            "金": 2,
            "木": 2,
            "水": 1,
            "火": 2,
            "土": 3
        },
        "当前大运": "癸亥 (2021-2031)"
    }
    return bazi_info


# --- Streamlit 页面配置 ---
st.set_page_config(page_title="AI 八字分析", layout="centered")
st.title("🔮 AI 八字排盘与分析")

# 用户输入出生信息
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("姓名（可选）")
    gender = st.selectbox("性别", ["女", "男"])
with col2:
    birth_date = st.date_input("出生日期", value=datetime.date(1996, 3, 11))
    birth_time = st.time_input("出生时间", value=datetime.time(10, 0))

birth_place = st.text_input("出生地点（城市）", "Maidstone, Kent")

# --- 生成八字分析 ---
if st.button("✨ 生成八字分析"):
    with st.spinner("排盘中，请稍候..."):
        bazi_result = get_bazi_info(birth_date, birth_time, birth_place, gender)

        st.subheader("🌿 八字排盘结果")
        st.json(bazi_result)

        # AI 分析内容
        prompt = f"请根据以下八字信息为用户生成命理分析：\n{bazi_result}"
        openai.api_key = st.secrets["openai_api_key"]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_response = response["choices"][0]["message"]["content"]
        except openai.error.RateLimitError:
            ai_response = "❌ OpenAI 配额已超出，请检查 API 使用状态或更换 API 密钥。"

        st.subheader("📖 AI 命理解读")
        st.write(ai_response)

st.markdown("---")
st.caption("© 2025 八字AI团队 | 仅供娱乐与参考")
