# AI 八字网页版 MVP 原型 - 使用 Streamlit
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
from datetime import datetime as dt
import streamlit as st
import datetime
import openai


# 获取八字信息的函数import datetime
from lunarcalendar import Converter, Solar, Lunar

def get_bazi_info(birth_date, birth_time, birth_place, gender):
    user_datetime = datetime.datetime.combine(birth_date, birth_time)


    # Convert Solar to Lunar
    solar = Solar(user_datetime.year, user_datetime.month, user_datetime.day)
    lunar = Converter.Solar2Lunar(solar)

    lunar_year = lunar.year  # Accessing lunar year
    lunar_month = lunar.month  # Accessing lunar month
    lunar_day = lunar.day  # Accessing lunar day
    is_leap = lunar.isleap  # Check if it is a leap month

    # Return simulated Bazi info (you can replace it with actual logic)
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
        print(birth_date, birth_time, birth_place, gender)
        bazi_result = get_bazi_info(birth_date, birth_time, birth_place, gender)

        st.subheader("🌿 八字排盘结果")
        st.json(bazi_result)

        # AI 分析内容
        prompt = f"请根据以下八字信息为用户生成命理分析：binbin"# "\n{bazi_result}"
        openai.api_key = st.secrets["api_key"]
        #openai.api_key = st.secrets["openai"]["api_key"]

        try:
            # 使用简单的 API 调用进行测试
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, world!"}]
            )

            # 如果成功，返回响应
            print("API 连接成功！")
            print(response)

        except openai.OpenAIError as e:
            print("API 请求失败，错误信息：{e}")
        except Exception as e:
            print(f"发生错误: {e}")
        
        try:
            response = openai.completions.create(
                model="gpt-3.5-turbo-instruct", 
                prompt=prompt,
                max_tokens=100
            )
            ai_response = response['choices'][0]['text']
        except openai.OpenAIError as e:
            ai_response = f"❌ OpenAI API 错误: {e}"

        st.subheader("📖 AI 命理解读")
        st.write(ai_response)

st.markdown("---")
st.caption("© 2025 八字AI团队 | 仅供娱乐与参考")

