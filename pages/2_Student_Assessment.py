from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

def generate_assessment_pdf(
    academic_year,
    total_score,
    category,
    component_scores,
    strongest_area,
    weakest_area,
    improvement_tips,
    role_df
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1E3A8A"),
        fontSize=20,
        spaceAfter=15
    )

    elements = []

    elements.append(
        Paragraph("Student Readiness Assessment Report", title_style)
    )

    elements.append(Spacer(1, 15))

# Report Generation Date
    elements.append(
    Paragraph(
        f"<b>Report Generated:</b> {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
        styles["Normal"]
    )
)

    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
    f"<b>Academic Year:</b> {academic_year}",
    styles["Normal"]
))

    elements.append(Paragraph(
    f"<b>Overall Readiness Score:</b> {total_score:.2f}/100",
    styles["Normal"]
))

    elements.append(Paragraph(
    f"<b>Readiness Category:</b> {category}",
    styles["Normal"]
))

    elements.append(Spacer(1, 15))

    elements.append(Paragraph(
    "Component-wise Performance",
    styles["Heading2"]
))

    component_data = [
        ["Component", "Score", "Maximum Marks"]
    ]

    for area, (score, maximum) in component_scores.items():
        component_data.append([
            area,
            f"{score:.2f}",
            f"{maximum}"
        ])

    component_table = Table(
        component_data,
        colWidths=[250, 100, 100]
    )

    component_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#EFF6FF"))
    ]))

    elements.append(component_table)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph(
        "Performance Analysis",
        styles["Heading2"]
    ))

    elements.append(Paragraph(
        f"<b>Strongest Area:</b> {strongest_area}",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"<b>Area Needing Improvement:</b> {weakest_area}",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 15))

    elements.append(Paragraph(
        "Personalized Improvement Suggestions",
        styles["Heading2"]
    ))

    for area, tips in improvement_tips.items():
        elements.append(Paragraph(
            f"<b>{area}</b>",
            styles["Normal"]
        ))

        for tip in tips:
            elements.append(Paragraph(
                f"- {tip}",
                styles["Normal"]
            ))

        elements.append(Spacer(1, 6))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "Recommended Internship Roles",
        styles["Heading2"]
    ))

    if not role_df.empty:

        role_data = [
            ["Internship Role", "Match Score"]
        ]

        for _, role in role_df.iterrows():
            role_data.append([
                str(role["Internship Role"]),
                f'{role["Match Score"]}%'
            ])

        role_table = Table(
            role_data,
            colWidths=[300, 150]
        )

        role_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 8)
        ]))

        elements.append(role_table)

    else:
        elements.append(Paragraph(
            "No matching internship roles found.",
            styles["Normal"]
        ))

    elements.append(Spacer(1, 20))

    elements.append(Paragraph(
        "<i>Note: This is a rule-based readiness assessment. "
        "It does not predict actual internship or placement selection.</i>",
        styles["Italic"]
    ))
    def add_page_number(canvas, doc):
        canvas.saveState()

        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.grey)

        page_number = f"Page {doc.page}"

        canvas.drawRightString(
        A4[0] - 40,
        25,
        page_number
    )

        canvas.restoreState()
    doc.build(
    elements,
    onFirstPage=add_page_number,
    onLaterPages=add_page_number
    )

    buffer.seek(0)

    return buffer

BASE_DIR = Path(__file__).resolve().parent.parent
st.set_page_config(
    page_title="Student Assessment",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Internship Readiness App")

st.write(
    "Welcome! Complete your assessment to understand "
    "your internship and placement readiness."
)

st.divider()
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

    # Select Academic Year
    academic_year = st.selectbox(
        "Current Academic Year",
        ["1st Year", "2nd Year", "3rd Year", "4th Year"]
    )

    # 1. Academic Performance
    st.subheader("1. Academic Performance")

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
    year_weights = {
        "1st Year": {
            "academic": 30, "coding": 25,
            "technical": 30, "career": 15
        },
        "2nd Year": {
            "academic": 25, "coding": 30,
            "technical": 30, "career": 15
        },
        "3rd Year": {
            "academic": 20, "coding": 30,
            "technical": 30, "career": 20
        },
        "4th Year": {
            "academic": 20, "coding": 25,
            "technical": 25, "career": 30
        }
    }

    weights = year_weights[academic_year]

    # 1. Academic Score
    academic_percentage = (cgpa / 10) * 100
    academic_score = academic_percentage * weights["academic"] / 100

    # 2. Coding Score
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

    coding_percentage = (coding_numerator / coding_denominator) * 100
    coding_score = coding_percentage * weights["coding"] / 100

    # 3. Technical Skills Score
    language_percentage = (len(selected_languages) / len(languages)) * 100
    skill_percentage = (len(selected_skills) / len(skills)) * 100

    technical_percentage = (language_percentage + skill_percentage) / 2
    technical_score = technical_percentage * weights["technical"] / 100

    # 4. Career Engagement Score
    platform_percentage = (len(selected_platforms) / len(platforms)) * 100

    career_components = [(platform_percentage, 7)]

    if club != "Not Available":
        career_components.append(((int(club) / 3) * 100, 4))

    if event != "Not Available":
        career_components.append(((int(event) / 3) * 100, 4))

    career_percentage = (
        sum(score * weight for score, weight in career_components)
        / sum(weight for score, weight in career_components)
    )

    career_score = career_percentage * weights["career"] / 100

    # Overall Readiness Score
    total_score = (
        academic_score
        + coding_score
        + technical_score
        + career_score
    )

    # Readiness Categories
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
<h3 style="color:#1E293B !important; margin:0;">
Your Overall Readiness Score
</h3>
<h1 style="color:#1E293B !important; font-size:52px; margin:12px 0;">
{total_score:.2f}
<span style="font-size:22px; color:#1E293B !important;">/ 100</span>
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
        "Maximum Marks": [
            weights["academic"],
            weights["coding"],
            weights["technical"],
            weights["career"]
]
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
        "Academic Performance": (academic_score, weights["academic"]),
        "Coding Practice": (coding_score, weights["coding"]),
        "Technical Skills": (technical_score, weights["technical"]),
        "Career Engagement": (career_score, weights["career"])
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

    

    # Year-wise Personalized Improvement Suggestions

    improvement_tips_by_year = {
        "1st Year": {
            "Academic Performance": [
                "Build strong fundamentals in mathematics and core subjects.",
                "Follow a regular study timetable.",
                "Focus on understanding concepts rather than memorising."
            ],
            "Coding Practice": [
                "Start learning C, C++ or Python.",
                "Practise basic programming problems regularly.",
                "Understand loops, functions and arrays."
            ],
            "Technical Skills": [
                "Learn basic programming languages.",
                "Explore Git and basic computer science concepts.",
                "Start learning the fundamentals of DSA."
            ],
            "Career Engagement": [
                "Explore technical clubs and college activities.",
                "Attend beginner-friendly workshops.",
                "Start exploring different technology domains."
            ]
        },

        "2nd Year": {
            "Academic Performance": [
                "Strengthen your core CS and engineering subjects.",
                "Maintain consistent semester performance.",
                "Revise important concepts regularly."
            ],
            "Coding Practice": [
                "Practise DSA problems consistently.",
                "Improve problem-solving skills.",
                "Participate in coding contests."
            ],
            "Technical Skills": [
                "Build practical projects using your technical skills.",
                "Explore AI/ML, databases and web development.",
                "Improve your knowledge of Git and development tools."
            ],
            "Career Engagement": [
                "Participate in hackathons and technical events.",
                "Build a project portfolio.",
                "Explore internship opportunities and their requirements."
            ]
        },

        "3rd Year": {
            "Academic Performance": [
                "Maintain a good CGPA while focusing on practical learning.",
                "Revise important technical subjects.",
                "Balance academics with internship preparation."
            ],
            "Coding Practice": [
                "Practise interview-level DSA problems.",
                "Improve coding speed and accuracy.",
                "Take part in regular coding contests."
            ],
            "Technical Skills": [
                "Develop advanced projects in your chosen domain.",
                "Strengthen your technical specialisation.",
                "Work on practical implementation of concepts."
            ],
            "Career Engagement": [
                "Apply for internships and practical opportunities.",
                "Prepare a project portfolio and resume.",
                "Participate in technical interviews and networking events."
            ]
        },

        "4th Year": {
            "Academic Performance": [
                "Maintain your academic performance.",
                "Revise important core subjects for interviews.",
                "Manage academics and placement preparation together."
            ],
            "Coding Practice": [
                "Practise company-specific coding questions.",
                "Revise important DSA topics.",
                "Improve problem-solving under time constraints."
            ],
            "Technical Skills": [
                "Revise your strongest technical skills.",
                "Prepare to explain your projects clearly.",
                "Strengthen concepts required for your target roles."
            ],
            "Career Engagement": [
                "Prepare and update your resume.",
                "Practise mock interviews and HR questions.",
                "Apply for suitable jobs and placement opportunities."
            ]
        }
    }

    improvement_tips = improvement_tips_by_year[academic_year]

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
    st.markdown("---")
    st.subheader("📄 Download Your Assessment Report")
    area_percentages = {
        area: (score / maximum) * 100
        for area, (score, maximum) in component_scores.items()
    }

    strongest_area = max(area_percentages, key=area_percentages.get)
    weakest_area = min(area_percentages, key=area_percentages.get)
    pdf_buffer = generate_assessment_pdf(
        academic_year=academic_year,
        total_score=total_score,
        category=category,
        component_scores=component_scores,
        strongest_area=strongest_area,
        weakest_area=weakest_area,
        improvement_tips=improvement_tips,
        role_df=role_df
    )

    st.download_button(
        label="📥 Download Assessment Report (PDF)",
        data=pdf_buffer,
        file_name="Student_Readiness_Assessment_Report.pdf",
        mime="application/pdf"
    )
