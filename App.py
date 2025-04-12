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
if "projects" not in st.session_state:
    st.session_state.projects = []

# סגנון CSS לעיצוב מרשים
st.markdown("""
<style>
body { direction: rtl; text-align: right; font-family: Arial, sans-serif; }
.stApp { background-color: #f4f6f9; }
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
@media (max-width: 600px) {
    .stButton>button { font-size: 14px; padding: 10px; }
    .stColumn { margin-bottom: 1rem; }
    .card { padding: 15px; }
}
</style>
""", unsafe_allow_html=True)

# כותרת עם תמונה
st.image("https://via.placeholder.com/1200x300.png?text=בנה+ביתך+-+הפלטפורמה+שלך+לבנייה+פרטית", use_column_width=True)
st.title("בנה ביתך - ניהול בנייה פרטית 🏗️")

# פונקציה להרשמה
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
                st.error("משתמש כבר קיים עם אימייל זה!")
            elif name and email and password:
                st.session_state.users_db[email] = {
                    "name": name,
                    "password": password,  # לא מאובטח, נסיוני בלבד
                    "user_type": user_type
                }
                st.success(f"משתמש {name} נרשם בהצלחה! התחבר כדי להמשיך.")
            else:
                st.error("אנא מלא את כל השדות!")
        st.markdown('</div>', unsafe_allow_html=True)

# פונקציה לכניסה
def login():
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)

# דף ראשי
if st.session_state.user:
    st.header(f"ברוך הבא, {st.session_state.user} ({st.session_state.user_type})!")
    st.write("נהל את פרויקט הבנייה שלך בקלות וביעילות:")
    
    # תפריט ראשי עם כרטיסיות
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("מה תרצה לעשות?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("העלאת תכניות", key="upload_plan"):
            st.session_state.page = "העלאת תכניות"
            st.experimental_rerun()
    with col2:
        if st.button("צ'קליסט בנייה", key="checklist"):
            st.session_state.page = "צ'קליסט בנייה"
            st.experimental_rerun()
    with col3:
        if st.button("דירוג אנשי מקצוע", key="rating"):
            st.session_state.page = "דירוג אנשי מקצוע"
            st.experimental_rerun()
    
    st.subheader("רשימת בעלי מקצוע לתפוצה")
    profession = st.selectbox("בחר סוג בעל מקצוע", ["מהנדס קונסטרוקציה", "קבלן שלד", "יועץ אינסטלציה", "יועץ חמל", "מפקח בנייה"])
    if st.button("שלח בקשה לבעלי מקצוע"):
        st.success(f"בקשה נשלחה לכל {profession} ברשימה!")
    st.markdown('</div>', unsafe_allow_html=True)

    # תיאור הקלטות (תכניות שהועלו)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("הקלטות ותכניות")
    if st.session_state.projects:
        for project in st.session_state.projects:
            st.write(f"**{project['name']}** - הועלה על ידי {project['user']} בתאריך {project['date']}")
    else:
        st.info("עדיין לא הועלו תכניות. התחל עכשיו!")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("התנתק"):
        st.session_state.user = None
        st.session_state.user_type = None
        st.session_state.page = None
        st.experimental_rerun()

else:
    st.write("התחבר או הירשם כדי להתחיל:")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        login()
    
    with col2:
        register()

# ניהול עמודים
if "page" in st.session_state and st.session_state.user:
    page = st.session_state.page
else:
    page = None

# עמוד העלאת תכניות
if page == "העלאת תכניות" and st.session_state.user:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("העלאת תכניות ובקשת הצעות מחיר")
        project_name = st.text_input("שם הפרויקט")
        profession = st.selectbox("בחר סוג בעל מקצוע", ["מהנדס קונסטרוקציה", "קבלן שלד", "יועץ אינסטלציה", "יועץ חשמל", "מפקח בנייה"])
        uploaded_file = st.file_uploader("העלה תכנית (PDF/DWG)", type=["pdf", "dwg"])
        
        if uploaded_file:
            st.write(f"קובץ הועלה: {uploaded_file.name}")
            if st.button("פרסם בקשה להצעות"):
                st.session_state.projects.append({
                    "name": project_name,
                    "user": st.session_state.user,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "file": uploaded_file.name
                })
                st.success(f"בקשה ל-{profession} עבור {project_name} פורסמה!")
        st.markdown('</div>', unsafe_allow_html=True)

# עמוד צ'קליסט
elif page == "צ'קליסט בנייה" and st.session_state.user:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("צ'קליסט תהליך הבנייה")
        checklist = [
            "רכישת מגרש", "קבלת היתר בנייה", "תכנון אדריכלי", "תכנון קונסטרוקטיבי",
            "בניית שלד", "גמרים", "חיבור לתשתיות", "קבלת טופס 4"
        ]
        for item in checklist:
            checked = st.checkbox(item)
            if checked:
                st.write(f"✔️ {item} הושלם!")
        st.markdown('</div>', unsafe_allow_html=True)

# עמוד דירוג
elif page == "דירוג אנשי מקצוע" and st.session_state.user:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("דירוג אנשי מקצוע")
        professional_name = st.text_input("שם בעל המקצוע")
        rating = st.slider("דירוג (1-5)", 1, 5)
        comment = st.text_area("הערות (אנונימי)")
        if st.button("שלח דירוג"):
            st.success(f"דירוג עבור {professional_name} נשלח!")
        st.markdown('</div>', unsafe_allow_html=True)
