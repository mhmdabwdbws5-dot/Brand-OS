import json
import google.generativeai as genai
import streamlit as st

# إعداد مظهر الصفحة
st.set_page_config(
    page_title="Brand OS - المُفكّر", page_icon="🧠", layout="centered"
)

st.title("🧠 Brand OS: المُفكّر (صانع المحتوى)")
st.markdown(
    "ارفع ملف الـ `meta.json` اللي طلّعه الإلستريتور، واكتب سطرين على نشاط البراند، وخلي الذكاء الاصطناعي يكتبلك الدليل."
)

# 1. خانة مفتاح الـ API
api_key = st.text_input(
    "أدخل مفتاح Gemini API الخاص بك:",
    type="password",
    placeholder="AIzaSy...",
    help="تقدر تطلعه مجاناً من Google AI Studio",
)

# 2. رفع ملف الميتا
uploaded_file = st.file_uploader("ارفع ملف meta.json هنا:", type=["json"])

# 3. وصف النشاط
business_desc = st.text_area(
    "شنو نشاط هالبراند؟",
    placeholder="مثال: مطعم مأكولات بحرية فاخر في طرابلس، يستهدف العائلات ورجال الأعمال، يتميز بالأكل الطازج.",
    height=100,
)

if uploaded_file and business_desc and api_key:
    # قراءة الجسون
    data = json.load(uploaded_file)

    st.success(f"تم قراءة بيانات البراند: **{data['brand_name']}**")

    with st.expander("معاينة البيانات المسحوبة من الإلستريتور"):
        st.json(data)

    if st.button("✨ صياغة دليل الهوية البصرية الآن", type="primary"):
        with st.spinner("جاري عصر الدماغ وكتابة الفلسفة... ⏳"):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")

                colors_str = ", ".join(
                    [f"{c['name']} ({c['hex']})" for c in data["colors"]]
                )
                fonts_str = ", ".join(data["fonts"])

                prompt = f"""
                أنت خبير صياغة هويات بصرية (Brand Strategist & Copywriter).
                قم بكتابة "دليل الهوية البصرية" (Brand Guidelines Copy) للعلامة التجارية التالية:
                
                - اسم العلامة: {data['brand_name']}
                - مجال النشاط: {business_desc}
                - الألوان المستخرجة من التصميم: {colors_str}
                - الخطوط المستخدمة: {fonts_str}
                
                أريد النص باللغة العربية الفصحى الراقية والمقنعة تسويقياً، مقسماً إلى الأقسام التالية بوضوح:
                
                ## 1. قصة العلامة التجارية (Brand Story)
                [فقرة ملهمة تعبر عن الروح والرؤية]
                
                ## 2. نبرة الصوت (Tone of Voice)
                [3 صفات تصف طريقة مخاطبة البراند لجمهوره مع شرح قصير لكل صفة]
                
                ## 3. فلسفة الألوان (Color Rationale)
                [اشرح لماذا تم اختيار كل لون من الألوان المذكورة وكيف يخدم مجال النشاط نفسياً]
                
                ## 4. التوجيه الطباعي (Typography Logic)
                [اشرح دلالة استخدام الخطوط المذكورة في تعزيز شخصية البراند]
                
                ## 5. شعارات لفظية مقترحة (Taglines)
                [3 خيارات لـ Slogan قصير وجذاب]
                """

                response = model.generate_content(prompt)

                st.markdown("---")
                st.subheader("📜 المحتوى الجاهز:")
                st.write(response.text)

            except Exception as e:
                st.error(f"صار خطأ في الاتصال: {e}")
