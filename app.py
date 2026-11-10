
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Student Readiness Dashboard",
    page_icon="🎓",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv(BASE_DIR / "final_student_readiness_dataset.csv")

df = load_data()

st.markdown("""

<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #EEF2FF, #F5F3FF, #ECFEFF);
    color: #1E293B;
}

/* Main content */
.block-container {
    padding-top: 2rem;
}

/* All normal text */
.stApp p, .stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #334155;
}

/* Headings */
h1, h2, h3, h4 {
    color: #312E81 !important;
    font-weight: 750 !important;
}

/* Form labels */
.stApp .stTextInput label,
.stApp .stNumberInput label,
.stApp .stSelectbox label,
.stApp .stMultiSelect label,
.stApp .stSlider label,
.stApp .stRadio label {
    color: #312E81 !important;
    font-weight: 600 !important;
}

/* Input and dropdown fields */
.stApp input,
.stApp textarea,
.stApp [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #1E293B !important;
    border-color: #C7D2FE !important;
}

/* Dropdown text */
.stApp [data-baseweb="select"] * {
    color: #1E293B !important;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #FFFFFF, #E0E7FF);
    border: 1px solid #C7D2FE;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(79,70,229,0.10);
}

div[data-testid="stMetricValue"] {
    color: #4338CA !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #312E81, #6366F1);
}

/* Sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #4F46E5, #7C3AED);
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: 650;
}

hr {
    border-color: #C7D2FE;
}


/* Individual KPI card colors */

div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #DBEAFE, #EFF6FF) !important;
    border-left: 5px solid #2563EB !important;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #EDE9FE, #F5F3FF) !important;
    border-left: 5px solid #7C3AED !important;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(3) div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #FFEDD5, #FFF7ED) !important;
    border-left: 5px solid #EA580C !important;
}

div[data-testid="stHorizontalBlock"] > div:nth-child(4) div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #CCFBF1, #F0FDFA) !important;
    border-left: 5px solid #0D9488 !important;
}

</style>

""", unsafe_allow_html=True)

# Header
st.title("🎓 Student Internship & Placement Readiness Dashboard")
st.markdown(
    "Analyze student readiness, technical skills, coding practice "
    "and placement outcomes."
)

# Sidebar filter
st.sidebar.header("Dashboard Filters")

years = sorted(df["Academic Year"].dropna().unique())
selected_years = st.sidebar.multiselect(
    "Select Academic Year",
    years,
    default=years
)

filtered_df = df[df["Academic Year"].isin(selected_years)]

# KPI calculations
total_students = len(filtered_df)
avg_readiness = filtered_df["Overall_Readiness_Score"].mean()
needs_development = (
    filtered_df["Readiness_Category"] == "Needs Development"
).sum()
offers = (filtered_df["Offers_Received"] > 0).sum()

# KPI cards
st.subheader("📊 Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Students", total_students)
c2.metric("Average Readiness", f"{avg_readiness:.2f}/100")
c3.metric("Needs Development", int(needs_development))
c4.metric("Students Received Offers", int(offers))

st.divider()

# Readiness category chart
st.subheader("Readiness Category Distribution")

category_counts = (
    filtered_df["Readiness_Category"]
    .value_counts()
    .reindex(
        ["Needs Development", "Developing", "Progressing", "Strong"],
        fill_value=0
    )
)


import plotly.express as px

category_df = category_counts.reset_index()
category_df.columns = ["Readiness Category", "Students"]

color_map = {
    "Needs Development": "#F97316",
    "Developing": "#3B82F6",
    "Progressing": "#8B5CF6",
    "Strong": "#10B981"
}

fig = px.bar(
    category_df,
    x="Readiness Category",
    y="Students",
    color="Readiness Category",
    color_discrete_map=color_map,
    text="Students",
    title="Student Readiness Category Distribution"
)

fig.update_traces(
    textposition="outside",
    marker_line_width=0
)

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#312E81", size=13),
    showlegend=False,
    yaxis_title="Number of Students",
    xaxis_title="Readiness Category"
)


fig.update_layout(
    template="plotly_white",
    title=dict(
        text="Student Readiness Category Distribution",
        font=dict(size=21, color="#312E81"),
        x=0.02
    ),
    font=dict(
        family="Arial",
        size=14,
        color="#1E293B"
    ),
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    xaxis=dict(
        title=dict(font=dict(size=15, color="#1E293B")),
        tickfont=dict(size=13, color="#334155"),
        showgrid=False,
        showline=True,
        linecolor="#CBD5E1"
    ),
    yaxis=dict(
        title=dict(font=dict(size=15, color="#1E293B")),
        tickfont=dict(size=13, color="#334155"),
        gridcolor="#E2E8F0",
        zeroline=False
    ),
    margin=dict(l=30, r=30, t=75, b=60),
    height=480
)

fig.update_traces(
    textfont=dict(size=15, color="#1E293B")
)

st.plotly_chart(fig, use_container_width=True)



st.divider()

# Component performance
st.subheader("Component-wise Performance")

component_columns = {
    "Academic Performance": "Academic_Performance_Score",
    "Coding Practice": "Coding_Practice_Score",
    "Technical Skills": "Technical_Skills_Score",
    "Career Engagement": "Career_Engagement_Score"
}

component_data = pd.DataFrame({
    "Component": component_columns.keys(),
    "Average Score": [
        filtered_df[col].mean()
        for col in component_columns.values()
    ]
})


component_colors = {
    "Academic Performance": "#3B82F6",
    "Coding Practice": "#8B5CF6",
    "Technical Skills": "#14B8A6",
    "Career Engagement": "#F97316"
}

fig2 = px.bar(
    component_data,
    x="Average Score",
    y="Component",
    orientation="h",
    color="Component",
    color_discrete_map=component_colors,
    text="Average Score"
)

fig2.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside",
    textfont=dict(size=14, color="#1E293B")
)

fig2.update_layout(
    template="plotly_white",
    title=dict(
        text="Average Component-wise Performance",
        font=dict(size=21, color="#312E81")
    ),
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(size=14, color="#1E293B"),
    showlegend=False,
    xaxis=dict(
        title="Average Score",
        tickfont=dict(color="#334155"),
        gridcolor="#E2E8F0"
    ),
    yaxis=dict(
        title="",
        tickfont=dict(size=13, color="#334155"),
        categoryorder="total ascending"
    ),
    margin=dict(l=30, r=70, t=75, b=50),
    height=420
)

st.plotly_chart(fig2, use_container_width=True)


st.divider()
# Technical Skill Gap Analysis

st.header("💻 Technical Skill Gap Analysis")

recommendations = pd.read_csv(
    BASE_DIR / "skill_gap_recommendations.csv"
)

# Most reported skills
skill_columns = [
    col for col in df.columns
    if col.startswith("Skill_")
]

skill_counts = (
     filtered_df[skill_columns]
    .sum()
    .sort_values(ascending=False)
)

skill_counts.index = (
    skill_counts.index.str.replace("Skill_", "", regex=False)
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Most Reported Technical Skills")

    top_skills = skill_counts.head(10).reset_index()
    top_skills.columns = ["Skill", "Students"]


    fig5 = px.bar(
        top_skills.sort_values("Students"),
        x="Students",
        y="Skill",
        orientation="h",
        color="Students",
        color_continuous_scale=["#A5B4FC", "#4F46E5"],
        text="Students",
        title="Top 10 Technical Skills"
    )

    fig5.update_traces(
        textposition="outside",
        textfont=dict(color="#1E293B", size=12)
    )

    fig5.update_layout(
        template="plotly_white",
        font=dict(color="#1E293B"),
        title_font_color="#312E81",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        coloraxis_showscale=False,
        xaxis=dict(tickfont=dict(color="#334155"), gridcolor="#E2E8F0"),
        yaxis=dict(tickfont=dict(color="#334155")),
        height=430
    )

    st.plotly_chart(fig5, use_container_width=True)


with col2:
    st.subheader("Skills Needing Attention")

    gap_data = recommendations.sort_values(
        "Reporting Percentage",
        ascending=True
    ).head(10)


    fig6 = px.bar(
        gap_data.sort_values("Reporting Percentage", ascending=False),
        x="Reporting Percentage",
        y="Skill",
        orientation="h",
        color="Reporting Percentage",
        color_continuous_scale=["#FDBA74", "#EA580C"],
        text="Reporting Percentage",
        title="Skills Requiring Attention"
    )

    fig6.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        textfont=dict(color="#1E293B", size=12)
    )

    fig6.update_layout(
        template="plotly_white",
        font=dict(color="#1E293B"),
        title_font_color="#312E81",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        coloraxis_showscale=False,
        xaxis=dict(tickfont=dict(color="#334155"), gridcolor="#E2E8F0"),
        yaxis=dict(tickfont=dict(color="#334155")),
        height=430
    )

    st.plotly_chart(fig6, use_container_width=True)


# Recommendations table
st.subheader("🎯 Personalized Skill Recommendations")


st.dataframe(
    recommendations[
        ["Skill", "Students Reporting", "Reporting Percentage",
         "Recommended Action"]
    ].style.format({
        "Reporting Percentage": "{:.1f}%"
    }),
    column_config={
        "Skill": st.column_config.TextColumn("Technical Skill"),
        "Students Reporting": st.column_config.NumberColumn(
            "Students Reporting",
            format="%d"
        ),
        "Reporting Percentage": st.column_config.ProgressColumn(
            "Reporting Percentage",
            min_value=0,
            max_value=100,
            format="%.1f%%"
        ),
        "Recommended Action": st.column_config.TextColumn(
            "Recommended Action",
            width="large"
        )
    },
    use_container_width=True,
    hide_index=True
)

# Placement Comparison Analysis
st.divider()
st.header("🎯 Placement Readiness Analysis")

placement_df = filtered_df.copy()

placement_df["Placement Status"] = placement_df[
    "Offers_Received"
].apply(
    lambda x: "Received Offer" if x > 0 else "No Offer"
)

# Placement KPIs
placement_counts = (
    placement_df["Placement Status"]
    .value_counts()
    .reindex(["No Offer", "Received Offer"], fill_value=0)
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Placement Status Distribution")

    placement_chart_df = placement_counts.reset_index()
    placement_chart_df.columns = ["Placement Status", "Students"]

    fig3 = px.bar(
        placement_chart_df,
        x="Placement Status",
        y="Students",
        color="Placement Status",
        color_discrete_map={
            "No Offer": "#F97316",
            "Received Offer": "#10B981"
        },
        text="Students"
    )

    fig3.update_traces(
        textposition="outside",
        textfont=dict(size=14, color="#1E293B")
    )

    fig3.update_layout(
        template="plotly_white",
        title="Student Placement Status",
        title_font_color="#312E81",
        font=dict(color="#1E293B", size=13),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        showlegend=False,
        yaxis_title="Number of Students",
        xaxis_title="",
        height=380
    )


    fig3.update_xaxes(
        tickfont=dict(color="#1E293B", size=14),
        title_font=dict(color="#1E293B"),
        showline=True,
        linecolor="#64748B",
        showgrid=False
    )

    fig3.update_yaxes(
        tickfont=dict(color="#1E293B", size=14),
        title_font=dict(color="#1E293B"),
        gridcolor="#CBD5E1",
        zerolinecolor="#64748B"
    )

    st.plotly_chart(fig3, use_container_width=True)



with col2:
    st.subheader("Average Readiness by Placement Status")

    readiness_comparison = (
        placement_df.groupby("Placement Status")[
            "Overall_Readiness_Score"
        ].mean()
        .reindex(["No Offer", "Received Offer"])
        .dropna()
    )


    readiness_chart_df = readiness_comparison.reset_index()
    readiness_chart_df.columns = ["Placement Status", "Average Readiness"]

    fig4 = px.bar(
        readiness_chart_df,
        x="Placement Status",
        y="Average Readiness",
        color="Placement Status",
        color_discrete_map={
            "No Offer": "#3B82F6",
            "Received Offer": "#8B5CF6"
        },
        text="Average Readiness"
    )

    fig4.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        textfont=dict(size=14, color="#1E293B")
    )

    fig4.update_layout(
        template="plotly_white",
        title="Average Readiness Comparison",
        title_font_color="#312E81",
        font=dict(color="#1E293B", size=13),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        showlegend=False,
        yaxis_title="Average Readiness Score",
        xaxis_title="",
        height=380
    )


    fig4.update_xaxes(
        tickfont=dict(color="#1E293B", size=14),
        title_font=dict(color="#1E293B"),
        showline=True,
        linecolor="#64748B",
        showgrid=False
    )

    fig4.update_yaxes(
        tickfont=dict(color="#1E293B", size=14),
        title_font=dict(color="#1E293B"),
        gridcolor="#CBD5E1",
        zerolinecolor="#64748B"
    )

    st.plotly_chart(fig4, use_container_width=True)



# Detailed comparison
st.subheader("Placement-wise Readiness Summary")

summary = (
    placement_df.groupby("Placement Status")[
        "Overall_Readiness_Score"
    ]
    .agg(["count", "mean", "median"])
    .reset_index()
)

summary.columns = [
    "Placement Status",
    "Students",
    "Average Readiness",
    "Median Readiness"
]


st.dataframe(
    summary.style.format({
        "Average Readiness": "{:.2f}",
        "Median Readiness": "{:.2f}"
    }),
    column_config={
        "Students": st.column_config.NumberColumn(
            "Students",
            format="%d"
        ),
        "Average Readiness": st.column_config.ProgressColumn(
            "Average Readiness",
            min_value=0,
            max_value=100,
            format="%.2f"
        ),
        "Median Readiness": st.column_config.ProgressColumn(
            "Median Readiness",
            min_value=0,
            max_value=100,
            format="%.2f"
        )
    },
    use_container_width=True,
    hide_index=True
)


# Interactive Dataset Explorer
st.subheader("📚 Student Dataset Explorer")

search_text = st.text_input(
    "🔍 Search student records",
    placeholder="Enter keyword to search..."
)

dataset_columns = st.multiselect(
    "Select columns to display",
    options=filtered_df.columns.tolist(),
    default=filtered_df.columns.tolist()[:8]
)

explorer_df = filtered_df.copy()

if search_text:
    mask = explorer_df.astype(str).apply(
        lambda col: col.str.contains(
            search_text, case=False, na=False
        )
    ).any(axis=1)
    explorer_df = explorer_df[mask]

st.caption(f"Showing {len(explorer_df)} matching records")

if dataset_columns:
    st.dataframe(
        explorer_df[dataset_columns],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Please select at least one column.")

st.caption("Student Readiness Analysis | Academic Project")
# ==========================================
# NEW STUDENT READINESS ASSESSMENT PORTAL
# ==========================================

st.divider()
st.header("📝 New Student Readiness Assessment")

st.write(
    "Complete the assessment to calculate your "
    "Internship and Placement Readiness Score."
)

# Original dataset feature names
# Programming and Technical Languages
languages = [
    "C", "C++", "Python", "Java", "JavaScript",
    "C#", "SQL", "HTML", "CSS", "TypeScript", "Kotlin"
]

# Technical and Soft Skills
skills = [
    "DSA", "Machine Learning", "Deep Learning",
    "AI", "Web Development",
    "Data Analysis", "DBMS", "Operating Systems",
    "Git", "Cloud Computing", "Cybersecurity",
    "Communication", "Teamwork", "Leadership",
    "Problem Solving", "Public Speaking",
    "Time Management", "Hackathons", "Creativity"
]

platforms = [
    "LeetCode", "Codeforces", "CodeChef", "AtCoder",
    "HackerRank", "GeeksforGeeks", "Coding Ninjas", "Other"
]

with st.form("student_assessment"):

    # 1. Academic Performance
    st.subheader("1. Academic Performance")

    cgpa = st.number_input(
        "Current CGPA",
        min_value=0.0,
        max_value=10.0,
        value=7.0,
        step=0.1
    )

    # 2. Coding Practice
    st.subheader("2. Coding Practice")

    coding_hours = st.number_input(
        "Coding Hours per Week",
        min_value=0,
        max_value=100,
        value=0
    )

    weekly_problems = st.number_input(
        "Problems Solved per Week",
        min_value=0,
        max_value=1000,
        value=0
    )

    total_problems = st.number_input(
        "Total Problems Solved",
        min_value=0,
        max_value=100000,
        value=0
    )

    
    not_rated = st.checkbox(
        "I am not rated in Competitive Programming"
    )

    cp_rating = None
    cp_platform = None

    if not not_rated:

        cp_platform = st.selectbox(
            "Competitive Programming Platform",
            [
                "LeetCode",
                "Codeforces",
                "CodeChef",
                "AtCoder",
                "HackerRank",
                "GeeksforGeeks",
                "Coding Ninjas",
                "Other"
            ]
        )

        cp_rating = st.number_input(
            "Competitive Programming Rating",
            min_value=1,
            max_value=4000,
            value=1,
            step=1
        )

    contest = st.selectbox(
        "Contest Participation Frequency",
        ["Not Available", "Never", "Rarely", "Monthly", "Weekly"],
        index=0
    )


    # 3. Technical Skills
    st.subheader("3. Technical Skills")

    selected_languages = st.multiselect(
        "Select Languages You Know",
        languages
    )

    selected_skills = st.multiselect(
        "Select Your Technical and Soft Skills",
        skills
    )

    # 4. Career Engagement
    st.subheader("4. Career Engagement")

    selected_platforms = st.multiselect(
        "Select Coding Platforms You Use",
        platforms
    )

    club = st.selectbox(
        "Club Participation",
        ["Not Available", "0", "1", "2", "3"]
    )

    event = st.selectbox(
        "How Much Have Events Increased Your Interest?",
        ["Not Available", "0", "1", "2", "3"]
    )

    submitted = st.form_submit_button(
        "Calculate My Readiness Score"
    )


# ==========================================
# SCORE CALCULATION
# ==========================================

if submitted:

    # Academic Score out of 20
    academic_score = (cgpa / 10) * 20

    # Coding normalized features
    coding_features = {
        "hours": (min(max(coding_hours / 5, 0), 1), 8),
        "weekly": (min(max(weekly_problems / 5, 0), 1), 8),
        "total": (
            min(max(np.log1p(total_problems) / np.log1p(1300), 0), 1), 7
        ),
    }

    if cp_rating is not None:
        cp_score = min(cp_rating / 4000, 1)
        coding_features["cp"] = (cp_score, 7)
    else:
        coding_features["cp"] = (0, 7)

    if contest != "Not Available":
        contest_value = {
            "Never": 0, "Rarely": 1, "Monthly": 2, "Weekly": 4
        }[contest]
        coding_features["contest"] = (contest_value / 4, 5)

    coding_numerator = sum(
        score * weight for score, weight in coding_features.values()
    )
    coding_denominator = sum(
        weight for score, weight in coding_features.values()
    )
    coding_score = (coding_numerator / coding_denominator) * 35

    # Technical Skills Score out of 30
    language_score = (len(selected_languages) / len(languages)) * 15
    skill_score = (len(selected_skills) / len(skills)) * 15
    technical_score = language_score + skill_score

    # Career Engagement Score out of 15
    platform_score = (len(selected_platforms) / len(platforms)) * 7

    career_components = [(platform_score, 7)]

    if club != "Not Available":
        career_components.append(((int(club) / 3) * 4, 4))

    if event != "Not Available":
        career_components.append(((int(event) / 3) * 4, 4))

    career_score = (
        sum(score for score, weight in career_components)
        / sum(weight for score, weight in career_components)
    ) * 15

    # Overall Readiness Score
    total_score = (
        academic_score
        + coding_score
        + technical_score
        + career_score
    )

    # Project-defined readiness categories
    if total_score < 25:
        category = "Needs Development"
    elif total_score < 50:
        category = "Developing"
    elif total_score < 75:
        category = "Progressing"
    else:
        category = "Strong"

    # Display Results
    st.divider()
    st.header("🎯 Your Readiness Assessment Result")

    score_color = (
        "#10B981" if total_score >= 75
        else "#8B5CF6" if total_score >= 50
        else "#3B82F6" if total_score >= 25
        else "#F97316"
    )

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #DBEAFE, #EDE9FE);
            padding: 28px;
            border-radius: 18px;
            text-align: center;
            margin-bottom: 25px;
        ">
            <h3 style="color:#312E81 !important; margin:0;">
                Your Overall Readiness Score
            </h3>
            <h1 style="color:#312E81 !important; font-size:52px; margin:12px 0;">
                {total_score:.2f}
                <span style="font-size:22px;">/ 100</span>
            </h1>
            <div style="
                background:{score_color};
                display:inline-block;
                padding:8px 22px;
                border-radius:25px;
                font-weight:bold;
                color:white;
            ">
                {category}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📊 Component-wise Performance")

    result_df = pd.DataFrame({
        "Component": [
            "Academic Performance",
            "Coding Practice",
            "Technical Skills",
            "Career Engagement"
        ],
        "Your Score": [
            academic_score,
            coding_score,
            technical_score,
            career_score
        ],
        "Maximum Marks": [20, 35, 30, 15]
    })

    result_df["Percentage"] = (
        result_df["Your Score"] / result_df["Maximum Marks"] * 100
    )

    for _, row in result_df.iterrows():
        st.markdown(
            f"**{row['Component']}** — "
            f"{row['Your Score']:.2f} / {row['Maximum Marks']}"
        )
        st.progress(min(row["Percentage"] / 100, 1.0))

    st.info(
        "This is a rule-based readiness assessment "
        "using the project's scoring methodology. "
        "It is not a prediction of placement selection."
    )

    # ==========================================
    # PERSONALIZED IMPROVEMENT SUGGESTIONS

    st.markdown("---")
    st.header("🚀 Your Personalized Improvement Plan")

    component_scores = {
        "Academic Performance": (academic_score, 20),
        "Coding Practice": (coding_score, 35),
        "Technical Skills": (technical_score, 30),
        "Career Engagement": (career_score, 15)
    }

    normalized_scores = {
        name: (score / maximum) * 100
        for name, (score, maximum) in component_scores.items()
    }

    strongest = max(normalized_scores, key=normalized_scores.get)
    weakest = min(normalized_scores, key=normalized_scores.get)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style="background:#D1FAE5; padding:20px;
            border-radius:15px; border-left:6px solid #10B981;">
                <h4 style="color:#065F46;">🌟 Strongest Area</h4>
                <h3 style="color:#064E3B;">{strongest}</h3>
                <h2 style="color:#047857;">
                    {normalized_scores[strongest]:.1f}%
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background:#FFEDD5; padding:20px;
            border-radius:15px; border-left:6px solid #F97316;">
                <h4 style="color:#9A3412;">🎯 Priority Area</h4>
                <h3 style="color:#7C2D12;">{weakest}</h3>
                <h2 style="color:#C2410C;">
                    {normalized_scores[weakest]:.1f}%
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("📌 Recommended Actions")

    improvement_tips = {
        "Academic Performance": [
            "Follow a consistent study timetable.",
            "Revise core engineering and mathematics subjects.",
            "Work on improving semester performance."
        ],
        "Coding Practice": [
            "Practice DSA problems regularly.",
            "Solve problems on coding platforms.",
            "Participate in coding contests."
        ],
        "Technical Skills": [
            "Learn programming and development tools.",
            "Build projects using your technical skills.",
            "Explore databases, AI/ML and relevant technologies."
        ],
        "Career Engagement": [
            "Participate in technical clubs and events.",
            "Create and maintain a coding portfolio.",
            "Attend workshops and internship sessions."
        ]
    }

    for area, (score, maximum) in component_scores.items():
        percentage = (score / maximum) * 100

        if percentage < 50:
            status = "Needs Attention"
            color = "#F97316"
            background = "#FFF7ED"
            tips = improvement_tips[area]

        elif percentage < 75:
            status = "Scope for Improvement"
            color = "#D97706"
            background = "#FEFCE8"
            tips = [improvement_tips[area][0]]

        else:
            status = "Good Progress"
            color = "#059669"
            background = "#ECFDF5"
            tips = ["Continue practising to maintain this performance."]

        tips_html = "".join(
            f"<li style='margin:7px 0;'>{tip}</li>"
            for tip in tips
        )

        st.markdown(
            f"""
            <div style="background:{background}; padding:18px;
            border-radius:13px; margin:12px 0;
            border-left:5px solid {color};">
                <h4 style="color:{color}; margin-top:0;">
                    {area} — {status}
                </h4>
                <ul style="color:#334155; margin-bottom:0;">
                    {tips_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("💡 Skills You Can Explore")

    missing_skills = [
        skill for skill in skills
        if skill not in selected_skills
    ]

    if missing_skills:
        st.info(
            "Based on your selected skills, you can explore: "
            + ", ".join(missing_skills)
        )
    else:
        st.success("You have selected all listed skills!")

    # ==========================================
    # INTERNSHIP ROLE RECOMMENDATIONS
    # ==========================================

    st.markdown("---")
    st.header("🎯 Recommended Internship Roles")

    role_requirements = {
        "Data Analyst Intern": {
            "skills": ["Python", "SQL", "Data Analysis"],
            "languages": ["Python", "SQL"]
        },
        "AI/ML Intern": {
            "skills": ["Python", "Machine Learning", "Deep Learning", "AI"],
            "languages": ["Python"]
        },
        "Software Development Intern": {
            "skills": ["DSA", "Problem Solving", "DBMS", "Git"],
            "languages": ["C", "C++", "Java", "Python"]
        },
        "Web Development Intern": {
            "skills": ["Web Development", "Git"],
            "languages": ["HTML", "CSS", "JavaScript", "TypeScript"]
        },
        "Cloud Computing Intern": {
            "skills": ["Cloud", "Python", "Git"],
            "languages": ["Python", "Java"]
        },
        "Cybersecurity Intern": {
            "skills": ["Cybersecurity", "Operating Systems", "DBMS"],
            "languages": ["Python", "C", "C++"]
        }
    }

    role_results = []

    for role, requirements in role_requirements.items():

        required_skills = requirements["skills"]
        required_languages = requirements["languages"]

        matched_skills = [
            s for s in required_skills
            if s in selected_skills
        ]

        matched_languages = [
            lang for lang in required_languages
            if lang in selected_languages
        ]

        total_requirements = (
            len(required_skills) + len(required_languages)
        )

        matched_count = len(matched_skills) + len(matched_languages)

        match_percentage = (
            matched_count / total_requirements
        ) * 100

        role_results.append({
            "Internship Role": role,
            "Match Score": round(match_percentage, 1),
            "Matched Skills": ", ".join(matched_skills) or "None",
            "Matched Languages": ", ".join(matched_languages) or "None"
        })

    role_df = pd.DataFrame(role_results)

    role_df = role_df.sort_values(
        by="Match Score", ascending=False
)

    role_df = role_df[
        role_df["Match Score"] > 0
    ].reset_index(drop=True)

    st.write(
        "These suggestions are based on the skills and "
        "programming languages selected in your assessment."
    )

    if not role_df.empty and role_df["Match Score"].max() > 0:

        st.subheader("📊 Your Role Match Results")

        for _, role in role_df.iterrows():

            match = role["Match Score"]

            if match >= 75:
                color = "#059669"
                background = "#ECFDF5"
                status = "Excellent Match"
            elif match >= 50:
                color = "#7C3AED"
                background = "#F5F3FF"
                status = "Good Match"
            elif match >= 25:
                color = "#2563EB"
                background = "#EFF6FF"
                status = "Developing Match"
            else:
                color = "#EA580C"
                background = "#FFF7ED"
                status = "Explore This Area"

            st.markdown(
                f"""
                <div style="
                    background:{background};
                    padding:18px;
                    border-radius:14px;
                    margin:12px 0;
                    border-left:5px solid {color};
                ">
                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    flex-wrap:wrap;
                ">
                    <h4 style="color:#1E293B; margin:0;">
                        {role['Internship Role']}
                    </h4>
                    <h3 style="color:{color}; margin:5px 0;">
                        {match:.1f}%
                    </h3>
                </div>
                <p style="color:{color}; font-weight:bold;">
                    {status}
                </p>
                <p style="color:#334155;">
                    <b>Matched Skills:</b> {role['Matched Skills']}
                </p>
                <p style="color:#334155; margin-bottom:0;">
                    <b>Matched Languages:</b>
                    {role['Matched Languages']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
            )

        st.progress(min(match / 100, 1.0))

        best_role = role_df.iloc[0]

        st.success(
            f"Your highest matching role is: "
            f"{best_role['Internship Role']} "
            f"({best_role['Match Score']}% match)"
        )

    else:
        st.info(
            "No matching internship role found. "
            "Select relevant technical skills and programming "
            "languages to explore suitable roles."
        )
    st.caption(
        "Match scores indicate skill overlap, not actual "
        "internship eligibility or selection probability."
    )
