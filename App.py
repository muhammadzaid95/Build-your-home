
import streamlit as st
from datetime import datetime

# הגדרות עמוד
st.set_page_config(page_title="בנה ביתך", layout="wide")

# אתחול משתני מצב
for key, default in {
    "user": None,
    "user_type": None,
    "users_db": {},
    "projects": [],
    "page": None,
    "do_rerun": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# טיפול בריענון – רק לאחר אתחול ה־session_state
if st.session_state.do_rerun:
    st.session_state.do_rerun = False
    st.experimental_rerun()

# עיצוב CSS
st.markdown("""
<style>
body { direction: rtl; text-align: right; font-family: Arial, sans-serif; }
.stApp { background-color: #eef2f5; }
h1, h2, h3 { color: #2c3e50; }
.stButton>button {
    background-color: #3498db;
    color: white;
    border-radius: 8px;
    padding: 12px;
    font-size: 16px;
    width: 100%;
    transition: background-color 0.3s;
}
.stButton>button:hover {
    background-color: #2980b9;
}
.stTextInput>div>input, .stSelectbox>div>select {
    text-align: right;
    border-radius: 5px;
    padding: 10px;
}
.stFileUploader {
    border: 2px dashed #3498db;
    border-radius: 8px;
    padding: 10px;
}
.card {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    padding: 20px;
    margin-bottom: 20px;
}
hr { border: none; height: 1px; background-color: #ccc; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# כותרת
st.image("https://via.placeholder.com/1200x300.png?text=בנה+ביתך+-+הפלטפורמה+שלך+לבנייה+פרטית", use_column_width=True)
st.title("בנה ביתך - הפלטפורמה שלך לבנייה פרטית 🏗️")

# פונקציית התחברות
def login():
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("התחברות")
        email = st.text_input("אימייל", key="login_email")
        password = st.text_input("סיסמה", type="password", key="login_password")
        if st.button("התחבר"):
            user = st.session_state.users_db.get(email)
            if user and user["password"] == password:
                st.session_state.user = user["name"]
                st.session_state.user_type = user["user_type"]
                st.session_state.do_rerun = True
            else:
                st.error("אימייל או סיסמה שגויים!")
        st.markdown('</div>', unsafe_allow_html=True)

# פונקציית הרשמה
def register():
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("הרשמה")
        name = st.text_input("שם מלא", key="reg_name")
        email = st.text_input("אימייל", key="reg_email")
        password = st.text_input("סיסמה", type="password", key="reg_password")
        user_type = st.selectbox("סוג משתמש", ["בעל בית", "קבלן", "מהנדס", "ספק"], key="reg_user_type")
        if st.button("צור משתמש"):
            if email in st.session_state.users_db:
                st.error("משתמש עם אימייל זה כבר קיים.")
            elif name and email and password:
                st.session_state.users_db[email] = {
                    "name": name,
                    "password": password,
                    "user_type": user_type
                }
                st.success("ההרשמה הושלמה! עכשיו תוכל להתחבר.")
            else:
                st.error("אנא מלא את כל השדות.")
        st.markdown('</div>', unsafe_allow_html=True)

# ממשק ראשי
if st.session_state.user:
    st.markdown(f'<div class="card">', unsafe_allow_html=True)
    st.subheader(f"שלום {st.session_state.user} ({st.session_state.user_type})")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("העלאת תכניות"):
            st.session_state.page = "upload"
            st.experimental_rerun()
    with col2:
        if st.button("צ'קליסט בנייה"):
            st.session_state.page = "checklist"
            st.experimental_rerun()
    with col3:
        if st.button("דירוג בעלי מקצוע"):
            st.session_state.page = "rating"
            st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("התנתק"):
        st.session_state.user = None
        st.session_state.user_type = None
        st.session_state.page = None
        st.experimental_rerun()

else:
    st.write("התחבר או הירשם כדי להתחיל:")
    col1, col2 = st.columns(2)
    with col1:
        login()
    with col2:
        register()

# דפי משנה
if st.session_state.user:
    page = st.session_state.page

    if page == "upload":
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.header("העלאת תכניות")
            project_name = st.text_input("שם הפרויקט")
            profession = st.selectbox("סוג בעל מקצוע נדרש", ["מהנדס קונסטרוקציה", "קבלן", "אדריכל", "פיקוח"])
            file = st.file_uploader("העלאת קובץ (PDF / DWG)", type=["pdf", "dwg"])
            if file and st.button("פרסם בקשה"):
                st.session_state.projects.append({
                    "name": project_name,
                    "user": st.session_state.user,
                    "profession": profession,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M")
                })
                st.success("הבקשה פורסמה!")
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "checklist":
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.header("צ'קליסט בנייה")
            steps = ["רכישת מגרש", "היתר בנייה", "תכנון אדריכלי", "תכנון קונסטרוקציה", "עבודות שלד", "עבודות גמר", "חיבור תשתיות", "טופס 4"]
            for s in steps:
                st.checkbox(s, key=s)
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "rating":
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.header("דירוג בעלי מקצוע")
            name = st.text_input("שם בעל מקצוע")
            score = st.slider("דירוג", 1, 5)
            notes = st.text_area("הערות (אנונימי)")
            if st.button("שלח דירוג"):
                st.success("הדירוג נשלח בהצלחה!")
            st.markdown('</div>', unsafe_allow_html=True)
