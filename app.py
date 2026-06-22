import json
import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="Brand OS - المُفكّر v2", page_icon="🧠", layout="centered"
)

st.title("🧠 Brand OS: المُفكّر (الإصدار المطور)")
st.markdown("تم تفعيل **كاشف الموديلات التلقائي** لتجاوز أخطاء الاتصال بقوقل.")

# 1. إدخال المفتاح
api_key = st.text_input(
    "أدخل مفتاح Gemini API:", type="password", placeholder="AIzaSy..."
)

# 2. كشف الموديلات المتاحة للمفتاح تلقائياً (X-Ray)
available_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
if api_key:
    try:
        genai.configure(api_key=api_key)
        # جلب الموديلات الحقيقية من حسابك
        live_models = [
            m.name.replace("models/", "")
            for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
        if live_models:
            available_models = live_models
    except Exception as e:
        st.error(f"⚠️ المفتاح فيه مشكلة أو غير مفعّل: {e}")

selected_model = st.selectbox(
    "اختر الموديل (هذه هي الموديلات المتاحة لمفتاحك فعلياً):",
    available_models,
)

# 3. رفع الملف والوصف
uploaded_file = st.file_uploader("ارفع ملف meta.json هنا:", type=["json"])
business_desc = st.text_area("شنو نشاط هالبراند؟", placeholder="اكتب هنا...")

if uploaded_file and business_desc and api_key:
    data = json.load(uploaded_file)

    if st.button("✨ صياغة دليل الهوية البصرية الآن", type="primary"):
        with st.spinner(f"جاري الاتصال بموديل {selected_model}... ⏳"):
            try:
                model = genai.GenerativeModel(selected_model)

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
                st.error(
                    f"فشل الاتصال بهذا الموديل، جرب اختر واحد ثاني من القائمة فوق! (السبب التقني: {e})"
                )
