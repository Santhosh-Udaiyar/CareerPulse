import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from prophet import Prophet
from matplotlib_venn import venn2
import matplotlib.pyplot as plt
from io import StringIO
import spacy

st.set_page_config(page_title="CareerPulse Dashboard", layout="wide")

# Sidebar theme controls
st.sidebar.title("🖌️ Theme Settings")
selected_theme = st.sidebar.selectbox("🌒 Seasonal Theme", ["Spring", "Summer", "Autumn", "Winter"])
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")

# Gradient setup
season_gradients = {
    "Spring": "linear-gradient(to right, #6b8e23, #3b6e3b)",
    "Summer": "linear-gradient(to right, #6a5acd, #483d8b)",
    "Autumn": "linear-gradient(to right, #8b4513, #5c3317)",
    "Winter": "linear-gradient(to right, #2f4f4f, #1c1c1c)"
}
dark_gradient = "linear-gradient(to right, #1e1e1e, #2c2c2c)"
active_gradient = dark_gradient if dark_mode else season_gradients[selected_theme]

# Inject CSS
st.markdown(f"""
    <style>
        .stApp {{
            background: {active_gradient};
            transition: background 1s ease;
        }}
        .feature-container {{
            background-color: #2b2b2b;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            padding: 30px;
            margin: 30px 0;
            color: #f0f0f0;
        }}
        .feature-container:hover {{ background-color: #3a3a3a; }}
        .feature-title {{ font-size: 24px; font-weight: bold; color: #ffffff; margin-bottom: 20px; }}
        .floating-nav {{
            position: fixed; top: 20px; right: 20px;
            background-color: #2e2e2e; border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2); padding: 15px; z-index: 999;
        }}
        .floating-nav select {{
            font-size: 16px; padding: 6px; border-radius: 6px;
            border: 1px solid #555; background-color: #1e1e1e; color: #f0f0f0;
        }}
    </style>
""", unsafe_allow_html=True)

# Floating nav
st.markdown('<div class="floating-nav"><label><strong>🔍 Jump to Feature</strong></label>', unsafe_allow_html=True)
selected_feature = st.selectbox("", [
    "Skill Demand Forecasting", "Resume Analyzer", "Geo Heatmap",
    "Salary Estimator", "Compare Roles", "Personalization & Growth"
], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("job_data.csv", parse_dates=["date"])
    df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
    df = df.dropna(subset=['salary'])
    df['salary'] = df['salary'].astype(int)
    df['skill'] = df['skill'].str.strip().replace({
        'powerbi': 'PowerBI', 'aws': 'AWS', 'sql': 'SQL', 'nlp': 'NLP',
        'pytorch': 'PyTorch', 'tensorflow': 'TensorFlow', 'spark': 'Spark',
        'excel': 'Excel', 'tableau': 'Tableau', 'python': 'Python'
    })
    return df

df = load_data()

# Feature modules
def skill_forecasting():
    st.markdown('<div class="feature-container"><div class="feature-title">📈 Skill Demand Forecasting</div>', unsafe_allow_html=True)
    skill = st.selectbox("Select a skill", sorted(df['skill'].unique()))
    skill_df = df[df['skill'] == skill].groupby('date').size().reset_index(name='count')
    skill_df = skill_df.rename(columns={'date': 'ds', 'count': 'y'})
    if len(skill_df) < 2:
        st.warning("Not enough data points to forecast.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    model = Prophet()
    model.fit(skill_df)
    future = model.make_future_dataframe(periods=6, freq='M')
    forecast = model.predict(future)
    fig = model.plot(forecast)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

def resume_analyzer():
    st.markdown('<div class="feature-container"><div class="feature-title">🧠 Resume Analyzer</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your resume (.txt)", type=["txt"])
    if uploaded_file:
        text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        extracted = [ent.text.lower() for ent in doc.ents if ent.label_ in ["SKILL", "ORG", "PRODUCT"]]
        trending = df['skill'].value_counts().head(20).index.tolist()
        matched = set(extracted) & set([s.lower() for s in trending])
        missing = set([s.lower() for s in trending]) - set(extracted)
        st.success(f"✅ Matched Skills: {', '.join(matched) if matched else 'None'}")
        st.warning(f"📌 Missing Trending Skills: {', '.join(missing) if missing else 'None'}")
    st.markdown('</div>', unsafe_allow_html=True)

def geo_heatmap():
    st.markdown('<div class="feature-container"><div class="feature-title">🗺️ Geo Heatmap</div>', unsafe_allow_html=True)
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="city", hover_data=["role", "skill", "salary"],
                            color="salary", size="salary", zoom=4, height=500)
    fig.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)

def salary_estimator():
    st.markdown('<div class="feature-container"><div class="feature-title">🧮 Salary Estimator</div>', unsafe_allow_html=True)
    role = st.selectbox("Select Role", sorted(df['role'].unique()))
    city = st.selectbox("Select City", sorted(df['city'].unique()))
    filtered = df[(df['role'] == role) & (df['city'] == city)]
    avg_salary = filtered['salary'].mean()
    st.metric("Estimated Salary", f"₹{int(avg_salary):,}" if not np.isnan(avg_salary) else "Data not available")
    st.markdown('</div>', unsafe_allow_html=True)

def compare_roles():
    st.markdown('<div class="feature-container"><div class="feature-title">⚔️ Compare Roles</div>', unsafe_allow_html=True)
    role_a = st.selectbox("Role A", sorted(df['role'].unique()), key="role_a")
    role_b = st.selectbox("Role B", sorted(df['role'].unique()), key="role_b")
    skills_a = set(df[df['role'] == role_a]['skill'].dropna().unique())
    skills_b = set(df[df['role'] == role_b]['skill'].dropna().unique())
    st.write("🧠 Skill Overlap")
    venn2([skills_a, skills_b], set_labels=(role_a, role_b))
    st.pyplot(plt)
    st.write("💰 Average Salary Comparison")
    salary_a = df[df['role'] == role_a]['salary'].mean()
    salary_b = df[df['role'] == role_b]['salary'].mean()
    fig = px.bar(x=[role_a, role_b], y=[salary_a, salary_b], labels={'x': 'Role', 'y': 'Average Salary'})
    st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)

def personalization_growth():
    st.markdown('<div class="feature-container"><div class="feature-title">🎨 Personalization & Growth</div>', unsafe_allow_html=True)
    st.markdown("### 🌗 Theme Settings\nUse the sidebar to toggle dark mode and choose seasonal backgrounds.")
    feedback = st.text_area("📣 Feedback")
    if st.button("Submit Feedback"): st.success("Thanks for your feedback!")
    st.info("🧠 Career Assistant (Coming Soon)")
    st.markdown('</div>', unsafe_allow_html=True)

# Router
if selected_feature == "Skill Demand Forecasting":
    skill_forecasting()
elif selected_feature == "Resume Analyzer":
    resume_analyzer()
elif selected_feature == "Geo Heatmap":
    geo_heatmap()
elif selected_feature == "Salary Estimator":
    salary_estimator()
elif selected_feature == "Compare Roles":
    compare_roles()
elif selected_feature == "Personalization & Growth":
    personalization_growth()