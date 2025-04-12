import streamlit as st
from datetime import datetime

# הגדרות עמוד
st.set_page_config(page_title="בנה ביתך", layout="wide")

# אתחול session state
if "user" not in st.session_state:
    st.session_state.user = None
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "users_db" not in st.session_state:
    st.session_state.users_db = {}
if "projects" not in st.session_state:
    st.session_state.projects = []
if "page" not in st.session_state:
    st.session_state.page = None

# סגנון עיצוב
st.markdown("""
<style>
body { direction: rtl; text-align: right; font-family: Arial; }
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
.stButton>button:hover { background-color: #2980b9; }
.stTextInput>div>input, .stSelectbox>div>select {
    text-align: right;
    border-radius: 5px;
    padding: 10px;
}
.card {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    padding: 20px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# כותרת
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
            st.error("משתמש כבר קיים עם אימייל זה.")
        elif name and email and password:
            st.session_state.users_db[email] = {
                "name": name,
                "password": password,
                "user_type": user_type
            }
            st.success(f"ההרשמה הושלמה! שלום {name}, כעת תוכל להתחבר.")
        else:
            st.error("אנא מלא את כל השדות.")
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
            st.experimental_rerun()
        else:
            st.error("אימייל או סיסמה שגויים.")
    st.markdown('</div>', unsafe_allow_html=True)

# פונקציה להצגת פרויקטים שהועלו
def show_projects():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("תכניות שהועלו")
    if st.session_state.projects:
        for project in st.session_state.projects:
            st.write(f"**{project['name']}** - מאת {project['user']} בתאריך {project['date']}")
    else:
        st.info("אין תכניות כרגע.")
    st.markdown('</div>', unsafe_allow_html=True)

# תוכן ראשי כשמשתמש מחובר
if st.session_state.user:
    st.header(f"שלום, {st.session_state.user} ({st.session_state.user_type})")
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
        if st.button("דירוג בעלי מקצוע"):
            st.session_state.page = "rating"
            st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # שליחת בקשה לבעלי מקצוע
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("שליחת בקשה לבעלי מקצוע")
    profession = st.selectbox("בחר מקצוע", ["מהנדס קונסטרוקציה", "קבלן שלד", "יועץ אינסטלציה", "יועץ חשמל", "מפקח בנייה"])
    if st.button("שלח בקשה"):
        st.success(f"הבקשה נשלחה לכל {profession}!")
    st.markdown('</div>', unsafe_allow_html=True)

    show_projects()

    if st.button("התנתק"):
        for key in ["user", "user_type", "page"]:
            st.session_state[key] = None
        st.experimental_rerun()

# תצוגה למשתמש לא מחובר
else:
    st.write("אנא התחבר או הירשם:")
    col1, col2 = st.columns(2)
    with col1:
        login()
    with col2:
        register()

# עמודים פנימיים
if st.session_state.page == "upload" and st.session_state.user:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("העלאת תכנית + בקשת הצעות מחיר")
    project_name = st.text_input("שם הפרויקט")
    profession = st.selectbox("בחר מקצוע", ["מהנדס קונסטרוקציה", "קבלן שלד", "יועץ אינסטלציה", "יועץ חשמל", "מפקח בנייה"])
    file = st.file_uploader("העלאת קובץ (PDF או DWG)", type=["pdf", "dwg"])
    if file and st.button("פרסם בקשה"):
        st.session_state.projects.append({
            "name": project_name,
            "user": st.session_state.user,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "filename": file.name
        })
        st.success(f"הבקשה ל-{profession} פורסמה עבור {project_name}.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "checklist":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("צ'קליסט בנייה")
    checklist_items = ["רכישת מגרש", "היתר בנייה", "תכנון אדריכלי", "קונסטרוקציה", "שלד", "מערכות", "גמרים", "טופס 4"]
    for item in checklist_items:
        st.checkbox(item)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "rating":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("דירוג בעלי מקצוע")
    name = st.text_input("שם בעל מקצוע")
    rating = st.slider("דירוג", 1, 5)
    comment = st.text_area("הערה (אנונימית)")
    if st.button("שלח דירוג"):
        st.success(f"דירוג עבור {name} התקבל!")
    st.markdown('</div>', unsafe_allow_html=True)
