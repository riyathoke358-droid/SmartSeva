import streamlit as st
import pandas as pd
from database import create_database, get_schemes

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Smartseva",
    page_icon="🇮🇳",
    layout="wide"
)

create_database()

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #f5f7fc;
}
.main-title {
    font-size: 38px;
    font-weight: bold;
    color: #172554;
}
.subtitle {
    color: #64748b;
    font-size: 17px;
}
div.stButton > button {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- GET DATA ----------------

rows = get_schemes()

columns = [
    "id", "name", "category", "description",
    "occupation", "min_age", "max_age",
    "max_income", "documents", "instructions",
    "official_url"
]

df = pd.DataFrame(rows, columns=columns)

# ---------------- SIDEBAR ----------------

st.sidebar.title("🇮🇳 SmartSeva")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Scheme Finder",
        "Eligibility Checker",
        "Application Guide"
    ]
)

st.sidebar.info(
    "Your guide to discovering government schemes."
)

# ---------------- HOME PAGE ----------------

if page == "Home":

    st.markdown(
        '<p class="main-title">Welcome to SmartSeva</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Making Government Schemes Easy for Everyone</p>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Available Demo Schemes", len(df))
    col2.metric("Categories", df["category"].nunique())
    col3.metric("Features", "4")

    st.subheader("What can you do?")

    a, b = st.columns(2)

    with a:
        st.info("🔎 Scheme Finder\n\nSearch schemes by name or category.")

        st.success(
            "✅ Eligibility Checker\n\n"
            "Find potentially relevant schemes using your profile."
        )

    with b:
        st.warning(
            "📄 Document Checklist\n\n"
            "Understand which documents may be required."
        )

        st.info(
            "📋 Application Guide\n\n"
            "Read application instructions and official links."
        )

    st.caption(
        "Demo version: replace illustrative records with verified "
        "government scheme information."
    )

# ---------------- SCHEME FINDER ----------------

elif page == "Scheme Finder":

    st.title("🔎 Find Government Schemes")

    search = st.text_input(
        "Search scheme name or category"
    )

    category = st.selectbox(
        "Select category",
        ["All"] + sorted(df["category"].unique().tolist())
    )

    result = df.copy()

    if search:
        result = result[
            result["name"].str.contains(
                search, case=False, na=False
            ) |
            result["description"].str.contains(
                search, case=False, na=False
            )
        ]

    if category != "All":
        result = result[result["category"] == category]

    if result.empty:
        st.warning("No matching schemes found.")

    for _, scheme in result.iterrows():

        with st.expander(scheme["name"]):

            st.write(scheme["description"])

            st.write("Category:", scheme["category"])

            st.write("Occupation:", scheme["occupation"])

            st.write("Age range:",
                     f'{scheme["min_age"]}–{scheme["max_age"]}')

            st.write(
                "Maximum income in demo rules:",
                f'₹{scheme["max_income"]:,.0f}'
            )

            st.write("Documents:", scheme["documents"])

            st.markdown(
                f'[Visit official portal]({scheme["official_url"]})'
            )

# ---------------- ELIGIBILITY CHECKER ----------------

elif page == "Eligibility Checker":

    st.title("✅ Eligibility Checker")

    st.write("Enter your details to find potentially relevant schemes.")

    age = st.number_input(
        "Enter your age",
        min_value=1,
        max_value=100,
        value=20
    )

    occupation = st.selectbox(
        "Select your occupation",
        [
            "Student",
            "Farmer",
            "Women",
            "Unemployed",
            "Other"
        ]
    )

    income = st.number_input(
        "Annual family income (₹)",
        min_value=0,
        value=100000,
        step=10000
    )

    if st.button("Find My Schemes"):

        matches = df[
            (df["min_age"] <= age) &
            (df["max_age"] >= age) &
            (df["max_income"] >= income) &
            (
                (df["occupation"] == occupation) |
                (df["occupation"] == "All")
            )
        ]

        st.subheader("Your Results")

        if len(matches) > 0:

            st.success(
                f"{len(matches)} potentially matching demo schemes found!"
            )

            for _, scheme in matches.iterrows():

                st.write("###", scheme["name"])

                st.write(scheme["description"])

                st.write(
                    "**Reason:** Your age, income and occupation "
                    "match the demonstration rules."
                )

                st.write("Documents:", scheme["documents"])

                st.markdown(
                    f'[Official portal]({scheme["official_url"]})'
                )

        else:

            st.warning(
                "No matching demo schemes found. "
                "Try another profile."
            )

        st.caption(
            "This is a basic demonstration, not an official "
            "eligibility determination."
        )

# ---------------- APPLICATION GUIDE ----------------

elif page == "Application Guide":

    st.title("📋 Application Guide")

    selected = st.selectbox(
        "Select a scheme",
        df["name"].tolist()
    )

    scheme = df[df["name"] == selected].iloc[0]

    st.subheader(scheme["name"])

    st.write("### Required Documents")

    documents = scheme["documents"].split(",")

    for document in documents:
        st.checkbox(document.strip(), key=f"doc_{document.strip()}")

    st.write("### Application Instructions")

    st.write(scheme["instructions"])

    st.write("### Official Website")

    st.markdown(
        f'[Open official portal]({scheme["official_url"]})'
    )

    st.info(
        "Always verify the latest eligibility and documents "
        "on the official scheme portal."
    )

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "SmartSeva| Hackathon Prototype | "
    "Making Government Schemes Accessible"
)