import streamlit as st

# הגדרות עמוד
st.set_page_config(page_title="בנה ביתך", layout="wide")

# אתחול מצב משתמש
if "user" not in st.session_state:
    st.session_state.user = None
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "users_db" not in st.session_state:
    st.session_state.users_db = {}

# כותרת
st.title("בנה ביתך - פלטפורמה לבנייה פרטית 🏗️")

# סרגל ניווט
if st.session_state.user:
    page = st.sidebar.selectbox("בחר עמוד", ["בית", "העלאת תכניות", "צ'קליסט בנייה", "דירוג אנשי מקצוע"])
else:
    page = "בית"

# פונקציה להרשמה
def register():
    st.header("הרשמה")
    name = st.text_input("שם מלא", key="reg_name")
    email = st.text_input("אימייל", key="reg_email")
    password = st.text_input("סיסמה", type="password", key="reg_password")
    user_type = st.selectbox("סוג משתמש", ["בעל בית", "קבלן", "מהנדס", "ספק"], key="reg_user_type")
    
    if st.button("צור משתמש"):
        if email in st.session_state.users_db:
            st.error("משתמש כבר קיים עם אימייל זה!")
        elif name and email and password:
            st.session_state.users_db[email] = {
                "name": name,
                "password": password,  # הערה: לא מאובטח, לשימוש נסיוני
                "user_type": user_type
            }
            st.success(f"משתמש {name} נרשם בהצלחה! התחבר כדי להמשיך.")
        else:
            st.error("אנא מלא את כל השדות!")

# פונקציה לכניסה
def login():
    st.header("התחברות")
    email = st.text_input("אימייל", key="login_email")
    password = st.text_input("סיסמה", type="password", key="login_password")
    
    if st.button("התחבר"):
        user_data = st.session_state.users_db.get(email)
        if user_data and user_data["password"] == password:
            st.session_state.user = user_data["name"]
            st.session_state.user_type = user_data["user_type"]
            st.success(f"ברוך הבא, {st.session_state.user} ({st.session_state.user_type})!")
            st.experimental_rerun()
        else:
            st.error("אימייל או סיסמה שגויים!")

# דף בית
if page == "בית":
    if st.session_state.user:
        st.header(f"ברוך הבא, {st.session_state.user} ({st.session_state.user_type})!")
        st.write("כאן תוכלו לנהל את תהליך הבנייה שלכם בקלות וביעילות:")
        st.markdown("""
        - **העלאת תכניות** ובקשת הצעות מחיר מקבלנים ויועצים.
        - **צ'קליסט** אינטראקטיבי לכל שלב בבנייה.
        - **דירוג** אנונימי של אנשי מקצוע.
        - חיבור לספקי חומרים והנחות.
        """)
        if st.button("התנתק"):
            st.session_state.user = None
            st.session_state.user_type = None
            st.experimental_rerun()
    else:
        st.write("התחבר או הירשם כדי להתחיל:")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            login()
        
        with col2:
            register()

# עמוד העלאת תכניות
elif page == "העלאת תכניות":
    if st.session_state.user:
        st.header("העלאת תכניות ובקשת הצעות מחיר")
        project_name = st.text_input("שם הפרויקט")
        profession = st.selectbox("בחר סוג בעל מקצוע", ["מהנדס קונסטרוקציה", "קבלן שלד", "יועץ אינסטלציה", "יועץ חשמל", "מפקח בנייה"])
        uploaded_file = st.file_uploader("העלה תכנית (PDF/DWG)", type=["pdf", "dwg"])
        
        if uploaded_file:
            st.write(f"קובץ הועלה: {uploaded_file.name}")
            if st.button("פרסם בקשה להצעות"):
                st.success(f"בקשה ל-{profession} עבור {project_name} פורסמה!")
    else:
        st.error("אנא התחבר כדי להשתמש בתכונה זו!")

# עמוד צ'קליסט
elif page == "צ'קליסט בנייה":
    if st.session_state.user:
        st.header("צ'קליסט תהליך הבנייה")
        checklist = [
            "רכישת מגרש", "קבלת היתר בנייה", "תכנון אדריכלי", "תכנון קונסטרוקטיבי",
            "בניית שלד", "גמרים", "חיבור לתשתיות", "קבלת טופס 4"
        ]
        for item in checklist:
            checked = st.checkbox(item)
            if checked:
                st.write(f"✔️ {item} הושלם!")
    else:
        st.error("אנא התחבר כדי להשתמש בתכונה זו!")

# עמוד דירוג
elif page == "דירוג אנשי מקצוע":
    if st.session_state.user:
        st.header("דירוג אנשי מקצוע")
        professional_name = st.text_input("שם בעל המקצוע")
        rating = st.slider("דירוג (1-5)", 1, 5)
        comment = st.text_area("הערות (אנונימי)")
        if st.button("שלח דירוג"):
            st.success(f"דירוג עבור {professional_name} נשלח!")
    else:
        st.error("אנא התחבר כדי להשתמש בתכונה זו!")

# תמיכה בכיווניות עברית ותצוגה במובייל
st.markdown("""
<style>
body { direction: rtl; text-align: right; }
.stButton>button { width: 100%; padding: 10px; }
.stTextInput>div>input { text-align: right; }
@media (max-width: 600px) {
    .stColumn { margin-bottom: 1rem; }
    .stButton>button { font-size: 16px; }
}
</style>
""", unsafe_allow_html=True)
