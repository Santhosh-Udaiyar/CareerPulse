import streamlit as st

# Page config
st.set_page_config(page_title="CareerPulse", page_icon="🧭", layout="wide")

# Sidebar theme controls
st.sidebar.title("🖌️ Theme Settings")
selected_theme = st.sidebar.selectbox("🌒 Seasonal Theme", ["Spring", "Summer", "Autumn", "Winter"])
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")

# Darker gradients
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
        .title {{
            text-align: center;
            font-size: 60px;
            font-weight: bold;
            color: #f5f5f5;
            margin-top: 20px;
        }}
        .tagline {{
            text-align: center;
            font-size: 22px;
            color: #dcdcdc;
            margin-bottom: 40px;
        }}
        .footer {{
            text-align: center;
            margin-top: 60px;
            font-size: 14px;
            color: #aaaaaa;
        }}
        .feature-box {{
            background-color: #2f2f2f;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            padding: 20px;
            text-align: center;
            font-size: 16px;
            font-weight: 500;
            color: #f0f0f0;
            transition: transform 0.3s ease, background-color 0.3s ease;
        }}
        .feature-box:hover {{
            transform: scale(1.05);
            background-color: #3f3f3f;
        }}
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            margin-top: 40px;
            padding: 0 40px;
        }}
    </style>
""", unsafe_allow_html=True)

# Logo and title
st.image("assets/careerpulse_logo.png", width=300)
st.markdown('<div class="title">CareerPulse</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Decode job trends. Design your future.</div>', unsafe_allow_html=True)

# Feature definitions
features = {
    "📈 Skill Demand Forecasting": """Analyze how the popularity of specific skills changes over time.
Use time-series modeling to predict future demand and trends.""",
    "🧠 Resume Analyzer": """Upload your resume to detect matching and missing trending skills.
Get personalized insights to improve your career readiness.""",
    "🗺️ Geo Heatmap": """Explore job density across cities and regions on an interactive map.
See where opportunities are concentrated for your chosen field.""",
    "🧮 Salary Estimator": """Estimate average salaries based on role, city, and selected skills.
Make informed decisions before interviews or job switches.""",
    "⚔️ Compare Roles": """Compare skills and salaries between two job roles.""",
    "🎨 Personalization & Growth": """Customize themes, submit feedback, and preview AI assistant.""",
    "📣 Feedback Center": "Share ideas to improve CareerPulse and request new features.",
    "👤 About the Creator": "CareerPulse is a mini project built by Navvodya."
}

# Feature grid
st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
for title, desc in features.items():
    st.markdown(f"""
        <div class="feature-box">
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Launch button
st.markdown("### 🚀 Ready to explore?")
st.page_link("pages/dashboard.py", label="Launch Dashboard", icon="📊")

# Testimonials
st.markdown("### 🧠 What users say")
st.markdown("""
> “CareerPulse helped me pivot from QA to Data Science with confidence.”  
> “I finally understood which skills were trending in my city.”  
> “The salary estimator gave me clarity before my interview.”
""")

# Feedback form
st.markdown("### 📣 Feedback")
feedback = st.text_area("What would you like to see improved or added?")
if st.button("Submit Feedback"):
    st.success("Thanks for your feedback! We'll use it to improve CareerPulse.")

# About the creator
st.markdown("### 👤 About the Creator")
st.markdown("""
CareerPulse is a mini project built by Navvodya. This project is proudly developed by a team of four Computer Science Engineering students — Shakthipriya, Bhavani, Yazhini, and Santhosh — currently in their 2nd year of study. Together, we’ve combined our curiosity, creativity, and coding skills to build a dashboard that helps users explore career trends, skill demand, and salary insights. CareerPulse reflects our shared vision of making data-driven career guidance more accessible and engaging. Connect on [GitHub](https://github.com/) or [LinkedIn](https://linkedin.com/).
""")

# Footer
st.markdown('<div class="footer">CareerPulse v1.0 • © 2025 S.P. • All rights reserved</div>', unsafe_allow_html=True)
st.markdown("""
### 🌐 Connect with Us
[![GitHub](https://img.shields.io/badge/GitHub-Navvodya-181717?style=for-the-badge&logo=github)](https://github.com/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Team-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/)
""", unsafe_allow_html=True)