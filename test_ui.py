#!/usr/bin/env python3
"""
Simple UI Test for InternHunt - Professional Styling Demo
"""

import streamlit as st
import pandas as pd
from styles import StyleManager

def main():
    """Main function to demonstrate the new UI"""
    
    # Set page config
    st.set_page_config(
        page_title="InternHunt - Resume Analyzer",
        page_icon="🎯",
        layout="wide",
    )
    
    # Initialize theme
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "dark"
    
    # Apply styles
    StyleManager.apply_global_styles()
    StyleManager.apply_theme_styles(st.session_state.theme_mode)
    
    # Professional sidebar styles
    st.markdown(f"""
        <style>
        /* Professional Sidebar Styles */
        .sb-chat-title {{
            font-weight: 700; 
            font-size: 1.125rem; 
            margin-bottom: 12px;
            color: inherit;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .sb-chip {{
            display: inline-block; 
            padding: 8px 12px; 
            border-radius: 20px; 
            font-size: 0.75rem; 
            font-weight: 600;
            margin-right: 8px; 
            margin-bottom: 6px;
            background: {StyleManager.COLORS['primary_gradient']};
            color: white;
            border: none;
            transition: all 0.2s ease;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    # Display header
    display_header()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Professional card demo
        st.markdown("""
            <div class="pro-card animate-fade-in">
                <div class="pro-card-header">
                    <div class="pro-card-icon">📄</div>
                    <h3 class="pro-card-title">Upload Your Resume</h3>
                </div>
                <p class="typography-body">
                    Upload your resume in PDF or Word format to get started with AI-powered analysis and personalized job recommendations.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'docx'],
            help="Supported formats: PDF, Word Document"
        )
        
        if uploaded_file:
            st.markdown("""
                <div class="pro-alert pro-alert-success">
                    <span style="font-size: 1.2rem;">✅</span>
                    <div>
                        <strong>File uploaded successfully!</strong><br>
                        <small>Your resume is ready for analysis.</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Demo skills display
            demo_skills()
            
            # Demo job listings
            demo_jobs()
    
    with col2:
        # Sidebar content
        st.markdown("""
            <div class="pro-card">
                <div class="pro-card-header">
                    <div class="pro-card-icon">💬</div>
                    <h3 class="pro-card-title">AI Assistant</h3>
                </div>
                <p class="typography-body">
                    Get personalized career advice and resume improvement suggestions from our AI assistant.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Theme toggle
        theme = st.toggle("🌙 Dark Mode" if st.session_state.theme_mode == "light" else "☀️ Light Mode")
        st.session_state.theme_mode = "light" if theme else "dark"
        StyleManager.apply_theme_styles(st.session_state.theme_mode)
        
        # Demo features
        st.markdown("""
            <div class="pro-card">
                <h4 class="typography-h3" style="margin-bottom: 1rem;">✨ Features</h4>
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div class="pro-badge pro-badge-primary">🔍 Smart Resume Analysis</div>
                    <div class="pro-badge pro-badge-success">🎯 Job Matching</div>
                    <div class="pro-badge pro-badge-warning">📊 Skill Assessment</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def display_header():
    """Display professional application header"""
    st.markdown(StyleManager.get_animation_styles(), unsafe_allow_html=True)
    
    # Professional header with modern design
    st.markdown(f"""
        <div class="animated-header" style="text-align: center; margin-bottom: 3rem; padding: 2rem 0;">
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;">
                <div style="
                    width: 64px; 
                    height: 64px; 
                    background: {StyleManager.COLORS['primary_gradient']}; 
                    border-radius: 16px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    margin-right: 20px;
                    box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4);
                ">
                    <span style="font-size: 28px; color: white;">🎯</span>
                </div>
                <div>
                    <h1 class="typography-h1" style="margin: 0; background: {StyleManager.COLORS['primary_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                        InternHunt
                    </h1>
                </div>
            </div>
            <h2 class="typography-h3" style="color: inherit; margin: 0 0 1rem 0; font-weight: 600; opacity: 0.8;">
                AI-Powered Resume Analyzer
            </h2>
            <p class="typography-body-large" style="color: inherit; max-width: 600px; margin: 0 auto; opacity: 0.7; line-height: 1.7;">
                Transform your career journey with intelligent resume analysis, personalized job recommendations, and skill insights powered by advanced AI.
            </p>
            
            <div class="pro-grid pro-grid-3" style="max-width: 800px; margin: 2rem auto 0; gap: 1rem;">
                <div class="pro-alert pro-alert-info" style="margin: 0; text-align: left;">
                    <span style="font-size: 1.2rem;">📊</span>
                    <div>
                        <strong>Smart Analysis</strong><br>
                        <small>AI-powered skill extraction</small>
                    </div>
                </div>
                <div class="pro-alert pro-alert-success" style="margin: 0; text-align: left;">
                    <span style="font-size: 1.2rem;">🎯</span>
                    <div>
                        <strong>Job Matching</strong><br>
                        <small>Personalized recommendations</small>
                    </div>
                </div>
                <div class="pro-alert pro-alert-warning" style="margin: 0; text-align: left;">
                    <span style="font-size: 1.2rem;">💬</span>
                    <div>
                        <strong>AI Assistant</strong><br>
                        <small>Interactive career guidance</small>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def demo_skills():
    """Demo skills display with professional styling"""
    st.markdown(StyleManager.get_skills_styles(), unsafe_allow_html=True)
    
    st.markdown("""
        <div class="skills-header animate-fade-in">
            <div class="skills-header-icon">🛠️</div>
            <h2 class="skills-header-text">SKILLS EXTRACTED</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Demo skills data
    categorized_skills = {
        "Technical Skills": ["Python", "JavaScript", "React", "Node.js", "SQL", "Git"],
        "Data Science/Analytics": ["Machine Learning", "Data Analysis", "Pandas", "NumPy", "Matplotlib"],
        "Soft Skills": ["Leadership", "Communication", "Problem Solving", "Team Collaboration"],
        "Design/Creative": ["Figma", "Adobe Photoshop", "UI/UX Design", "Wireframing"]
    }
    
    category_icons = {
        "Technical Skills": "💻",
        "Data Science/Analytics": "📊",
        "Soft Skills": "🤝",
        "Design/Creative": "🎨"
    }
    
    css_class_map = {
        "Technical Skills": "tech-skill",
        "Data Science/Analytics": "data-skill",
        "Soft Skills": "soft-skill",
        "Design/Creative": "design-skill"
    }
    
    html_output = '<div class="skills-container">'
    
    delay_counter = 0
    for category, skills in categorized_skills.items():
        if skills:
            icon = category_icons.get(category, "✨")
            css_class = css_class_map.get(category, "tech-skill")
            
            html_output += f'''
            <div class="skill-section animate-fade-in animate-delay-{min(delay_counter * 100, 400)}">
                <h3 class="skill-category">
                    <span class="category-icon">{icon}</span> {category}
                </h3>
                <div class="skills-grid">
            '''
            
            for skill in skills:
                html_output += f'<span class="skill-tag {css_class}">{skill}</span>'
            
            html_output += '</div></div>'
            delay_counter += 1
    
    html_output += '</div>'
    st.markdown(html_output, unsafe_allow_html=True)

def demo_jobs():
    """Demo job listings with professional styling"""
    st.markdown(StyleManager.get_job_listing_styles(), unsafe_allow_html=True)
    
    st.markdown("""
        <div class="skills-header animate-fade-in">
            <div class="skills-header-icon">💼</div>
            <h2 class="skills-header-text">RECOMMENDED JOBS</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Demo job data
    jobs = [
        {
            "title": "Frontend Developer",
            "company": "TechCorp Inc.",
            "location": "San Francisco, CA",
            "salary": "$80K - $120K",
            "description": "We're looking for a talented Frontend Developer to join our team and build amazing user experiences.",
            "skills": ["React", "JavaScript", "CSS", "HTML"]
        },
        {
            "title": "Data Scientist",
            "company": "DataFlow Solutions", 
            "location": "New York, NY",
            "salary": "$90K - $140K",
            "description": "Join our data science team to extract insights from complex datasets and build ML models.",
            "skills": ["Python", "Machine Learning", "Pandas", "SQL"]
        }
    ]
    
    for i, job in enumerate(jobs):
        skills_html = "".join([f'<span class="job-skill-tag">{skill}</span>' for skill in job["skills"]])
        
        st.markdown(f"""
            <div class="job-listing animate-fade-in animate-delay-{i * 100}">
                <div class="job-header">
                    <div>
                        <div class="job-title">
                            <div class="job-title-icon">💼</div>
                            {job["title"]}
                        </div>
                        <div class="job-company">{job["company"]}</div>
                        <div class="job-location">📍 {job["location"]}</div>
                    </div>
                    <div class="job-match-score">
                        ⭐ 95% Match
                    </div>
                </div>
                
                <div class="job-info-grid">
                    <div class="job-info-item">
                        <div class="job-info-icon">💰</div>
                        <div class="job-info-content">
                            <div class="job-info-label">Salary</div>
                            <div class="job-info-value">{job["salary"]}</div>
                        </div>
                    </div>
                    <div class="job-info-item">
                        <div class="job-info-icon">⏰</div>
                        <div class="job-info-content">
                            <div class="job-info-label">Type</div>
                            <div class="job-info-value">Full-time</div>
                        </div>
                    </div>
                    <div class="job-info-item">
                        <div class="job-info-icon">🏢</div>
                        <div class="job-info-content">
                            <div class="job-info-label">Experience</div>
                            <div class="job-info-value">2-4 years</div>
                        </div>
                    </div>
                </div>
                
                <p class="job-description">{job["description"]}</p>
                
                <div class="job-skills">
                    {skills_html}
                </div>
                
                <div class="job-actions">
                    <div class="job-salary">{job["salary"]}</div>
                    <a href="#" class="apply-button">
                        Apply Now ➤
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()