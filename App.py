import streamlit as st
from datetime import datetime

# הגדרות עמוד
st.set_page_config(page_title="בנה ביתך", layout="wide")

# טיפול בריענון
if "do_rerun" in st.session_state and st.session_state.do_rerun:
    st.session_state.do_rerun = False
    st.experimental_rerun()

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

# עיצוב CSS
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

# תמונת כותרת וכותרת ראשית
st.image("https://via.placeholder.com/1200x300.png?text=בנה+ביתך+-+הפלטפורמה+שלך+לבנייה+פרטית", use_column_width=True)
st.title("בנה ביתך - ניהול בנייה פרטית 🏗️")

# פונקציית הרשמה
def register():
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
                "password": password,
                "user_type": user_type
            }
            st.success("נרשמת בהצלחה! התחבר כדי להמשיך.")
        else:
            st.error("אנא מלא את כל השדות!")
    st.markdown('</div>', unsafe_allow_html=True)

# פונקציית התחברות
def login():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("התחברות")
    email = st.text_input("אימייל", key="login_email")
    password = st.text_input("סיסמה", type="password", key="login_password")

    if st.button("התחבר"):
        user_data = st.session_state.users_db.get(email)
        if user_data and user_data["password"] == password:
            st.session_state.user = user_data["name"]
            st.session_state.user_type = user_data["user_type"]
            st.session_state.do_rerun = True  # ריענון
        else:
            st.error("אימייל או סיסמה שגויים!")
    st.markdown('</div>', unsafe_allow_html=True)

# עמוד התחברות / הרשמה
if not st.session_state.user:
    st.write("התחבר או הירשם כדי להתחיל:")
    col1, col2 = st.columns(2)
    with col1: login()
    with col2: register()
    st.stop()

# עמוד ראשי
st.header(f"ברוך הבא, {st.session_state.user} ({st.session_state.user_type})!")
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("מה תרצה לעשות?")
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
    if st.button("דירוג אנשי מקצוע"):
        st.session_state.page = "rating"
        st.experimental_rerun()
st.markdown('</div>', unsafe_allow_html=True)

# שליחת בקשה לבעלי מקצוע
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("רשימת בעלי מקצוע לתפוצה")
profession = st.selectbox("בחר סוג בעל מקצוע", ["מהנדס קונסטרוקציה", "קבלן שלד", "יועץ אינסטלציה", "יועץ חשמל", "מפקח בנייה"])
if st.button("שלח בקשה לבעלי מקצוע"):
    st.success(f"הבקשה נשלחה לכל {profession} ברשימה!")
st.markdown('</div>', unsafe_allow_html=True)

# תכניות שהועלו
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("הקלטות ותכניות")
if st.session_state.projects:
    for p in st.session_state.projects:
        st.write(f"**{p['name']}** - הועלה ע״י {p['user']} בתאריך {p['date']}")
else:
    st.info("לא הועלו תכניות עדיין.")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("התנתק"):
    st.session_state.user = None
    st.session_state.user_type = None
    st.session_state.page = None
    st.session_state.do_rerun = True

# עמודים נוספים
if st.session_state.page == "upload":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("העלאת תכניות ובקשת הצעות מחיר")
    project_name = st.text_input("שם הפרויקט")
    profession = st.selectbox("בחר סוג בעל מקצוע", ["מהנדס קונסטרוקציה", "קבלן שלד", "יועץ אינסטלציה", "יועץ חשמל", "מפקח בנייה"])
    uploaded_file = st.file_uploader("העלה תכנית (PDF/DWG)", type=["pdf", "dwg"])
    
    if uploaded_file and st.button("פרסם בקשה להצעות"):
        st.session_state.projects.append({
            "name": project_name,
            "user": st.session_state.user,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "file": uploaded_file.name
        })
        st.success(f"בקשה ל-{profession} עבור '{project_name}' פורסמה!")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "checklist":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("צ'קליסט תהליך הבנייה")
    checklist = [
        "רכישת מגרש", "קבלת היתר בנייה", "תכנון אדריכלי", "תכנון קונסטרוקטיבי",
        "בניית שלד", "גמרים", "חיבור לתשתיות", "קבלת טופס 4"
    ]
    for item in checklist:
        st.checkbox(item, key=f"check_{item}")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "rating":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("דירוג אנשי מקצוע")
    name = st.text_input("שם בעל המקצוע")
    rating = st.slider("דירוג (1-5)", 1, 5)
    comment = st.text_area("הערות (אנונימי)")
    if st.button("שלח דירוג"):
        st.success(f"דירוג עבור {name} נשלח!")
    st.markdown('</div>', unsafe_allow_html=True)
