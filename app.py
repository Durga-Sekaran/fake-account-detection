import streamlit as st
from detection_logic import detect_account
import tempfile

# MUST be first Streamlit command
st.set_page_config(page_title="Fake Account Detection", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background-color: black; }
    h1 { font-size: 42px; color:white }
    p  { font-size: 20px; color:white }

    div.stButton > button {
        background-color: #1E40AF;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
    }

    div.stButton > button:hover {
        background-color: #1E3A8A;
    }

    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stMarkdownContainer"] p {
        color: white !important;
        font-size: 18px;
    }

    .stError { background-color:red }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align:center;color:white'>🔍 Fake Account Detection System</h1>",
    unsafe_allow_html=True
)

st.write("Enter account details to check whether an account is *FAKE or REAL*")

# ----------- USER INPUTS -----------
username = st.text_input("Username")

followers = st.number_input("Followers", min_value=0, step=1)
following = st.number_input("Following", min_value=0, step=1)
posts = st.number_input("Number of Posts", min_value=0, step=1)
account_age = st.number_input("Account Age (in days)", min_value=0, step=1)

bio = st.text_area("Bio")

uploaded_image = st.file_uploader(
    "Upload Profile Image",
    type=["jpg", "jpeg", "png"]
)

temp_image_path = ""

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Profile Image", width=200)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_image.read())
        temp_image_path = tmp.name

# ----------- DETECTION BUTTON -----------
if st.button("Detect Account"):

    account_data = {
        "followers": followers,
        "following": following,
        "posts": posts,
        "account_age_days": account_age,
        "bio": bio,
        "profile_image": temp_image_path
    }

    fake_percent, risk, reasons = detect_account(account_data)

    st.divider()
    st.subheader("📊 Detection Result")

    st.write(f"*Username:* {username}")
    st.write(f"*Fake Probability:* {fake_percent}%")
    st.write(f"*Real Probability:* {100 - fake_percent}%")
    st.write(f"*Risk Level:* {risk}")

    ratio = round(followers / following, 2) if following != 0 else followers
    st.write(f"*Followers–Following Ratio:* {ratio}")

    st.subheader("🧠 Reasons")
    if reasons:
        for r in reasons:
            st.write(f"- {r}")
    else:
        st.write("No suspicious patterns detected")

    if fake_percent >= 50:
        st.error("⚠ This account is likely *FAKE*")
    else:
        st.success("✅ This account is likely *REAL*")