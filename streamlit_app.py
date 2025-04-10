# streamlit_app.py

import streamlit as st
import datetime
from lunarcalendar import Converter, Solar
import openai
from fpdf import FPDF

# 设置页面
st.set_page_config(page_title="AI 八字分析", layout="centered")
st.title("🔮 AI 八字排盘与命理解读")

# AI 调用函数
def ask_openai(prompt):
    openai.api_key = st.secrets["api_key"]
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个八字命理专家"},
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ OpenAI API 错误: {e}"

# 导出为 PDF
def export_pdf(name, bazi_text, ai_analysis, liunian, minge):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # 使用中文字体（思源黑体或其他 TTF）
    pdf.add_font("Noto", "", "NotoSerifCJKsc-Regular", uni=True)
    pdf.set_font("Noto", size=12)
    
    def write_line(text): 
        pdf.multi_cell(0, 10, text)

    write_line(f"姓名：{name}")
    write_line("=== 八字排盘 ===")
    write_line(bazi_text)

    write_line("\n=== AI 命理解读 ===")
    write_line(ai_analysis)

    write_line("\n=== 📅 流年分析 ===")
    write_line(liunian)

    write_line("\n=== 🧬 命格分类 ===")
    write_line(minge)

    pdf.output("bazi_analysis.pdf")

    with open("bazi_analysis.pdf", "rb") as f:
        st.download_button("📄 下载分析报告 PDF", f, file_name="八字命理分析.pdf")

# 用户输入
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("姓名（可选）")
    gender = st.selectbox("性别", ["女", "男"])
with col2:
    birth_date = st.date_input("出生日期", min_value=datetime.date(1920, 1, 1), value=datetime.date(2000, 1, 1))
    birth_time = st.time_input("出生时间", value=datetime.time(12, 0))

birth_place = st.text_input("出生地点（城市）", "Melbourne")

# 主功能按钮
if st.button("✨ 生成八字分析"):
    with st.spinner("正在分析八字，请稍候..."):
        user_datetime = datetime.datetime.combine(birth_date, birth_time)
        solar = Solar(user_datetime.year, user_datetime.month, user_datetime.day)
        lunar = Converter.Solar2Lunar(solar)
        bazi_text = f"阳历: {user_datetime.strftime('%Y-%m-%d %H:%M')}\n农历: {lunar.year}年{lunar.month}月{lunar.day}日{'(闰)' if lunar.isleap else ''}\n出生地: {birth_place}\n性别: {gender}"

        # AI 获取四柱、五行、大运等信息
        bazi_prompt = f"请根据以下出生信息排出此人的四柱八字，并提供五行比例与当前大运：\n出生日期时间：{user_datetime.strftime('%Y-%m-%d %H:%M')}\n出生地：{birth_place}\n性别：{gender}"
        bazi_result = ask_openai(bazi_prompt)
        st.subheader("🌿 八字排盘结果")
        st.write(bazi_result)

        # AI 分析模块
        prompt_main = f"请根据以下八字信息为用户生成命理解读：\n{bazi_result}"
        ai_analysis = ask_openai(prompt_main)
        st.subheader("📖 AI 命理解读")
        st.write(ai_analysis)

        # 流年分析子模块
        liunian_prompt = f"请根据以下八字进行2025年的流年运势分析：\n{bazi_result}"
        liunian_analysis = ask_openai(liunian_prompt)
        st.subheader("📅 流年运势（2025）")
        st.write(liunian_analysis)

        # 命格分类子模块
        minge_prompt = f"根据以下八字信息，请判断此人的命格类别（如从强、从弱、正格等），并简要说明原因：\n{bazi_result}"
        minge_analysis = ask_openai(minge_prompt)
        st.subheader("🧬 命格分类")
        st.write(minge_analysis)

        # 导出 PDF
        export_pdf(name or "用户", bazi_result, ai_analysis, liunian_analysis, minge_analysis)

st.markdown("---")
st.caption("© 2025 八字AI团队 | 本应用仅供娱乐与参考使用")
