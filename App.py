#!/usr/bin/env python3
"""
InternHunt - Resume Analyzer Application
A comprehensive resume analysis tool with job recommendations and skill assessment.
"""

# Core libraries
import streamlit as st
import pandas as pd
import base64
import random
import time
import datetime
import os
import nltk
import joblib


# Import custom modules
from config import Config
from database import DatabaseManager
db_manager = DatabaseManager()
from api_services import JobAPIService, fetch_internshala_internships
from resume_parser import ResumeParser
from styles import StyleManager
from utils import AnalyticsUtils
from chat_service import chat_gemini, build_resume_context, check_gemini_health, get_suggested_questions
from streamlit.components.v1 import html as st_html  # legacy; floating chat removed
from job_scrapers import scrape_all, scrape_internshala, scrape_internshala_by_keywords
from Courses import (
    ds_course, web_course, android_course, ios_course, uiux_course,
    ai_course, cyber_course, cloud_course, data_eng_course, blockchain_course
)

import warnings
warnings.filterwarnings("ignore", message="coroutine 'expire_cache' was never awaited")

# -----------------------------
# ML Model Loading
# -----------------------------

@st.cache_resource
def load_resume_classifier():
    """Load the trained resume classification model (with version compatibility check)"""
    import sklearn

    try:
        data = joblib.load("resume_classifier_v2.pkl")

        # Handle both new and old formats safely
        if isinstance(data, dict) and "model" in data:
            model = data["model"]
            trained_version = data.get("sklearn_version", "unknown")

            # Optional warning if sklearn versions differ
            if trained_version != sklearn.__version__:
                st.warning(
                    f"⚠️ Model trained on scikit-learn {trained_version}, "
                    f"but running on {sklearn.__version__}. Retraining recommended if unexpected issues occur."
                )
        else:
            # fallback for older pickled models (without metadata)
            model = data

        return model

    except FileNotFoundError:
        st.error("❌ Model file not found. Please ensure 'resume_classifier_v2.pkl' exists in the project directory.")
        return None

    except Exception as e:
        st.warning(f"⚠️ Could not load ML model: {e}")
        return None


def predict_resume_category(resume_text, model=None):
    """Predict resume category and return top 3 predictions with probabilities"""
    if model is None:
        model = load_resume_classifier()
    
    if model is None:
        return None, []
    
    try:
        # Get prediction
        predicted_category = model.predict([resume_text])[0]
        
        # Get probabilities for top 3
        probabilities = model.predict_proba([resume_text])[0]
        classes = model.classes_
        
        # Get top 3 predictions
        top_3_idx = probabilities.argsort()[-3:][::-1]
        top_3_predictions = [
            {"category": classes[idx], "probability": probabilities[idx]}
            for idx in top_3_idx
        ]
        
        return predicted_category, top_3_predictions
    except Exception as e:
        st.error(f"Error predicting category: {e}")
        return None, []

def get_courses_by_category(predicted_category):
    """Get relevant courses based on predicted category"""
    category_course_map = {
        # --- Programming & Software ---
        'Java Developer': web_course + android_course,
        'Python Developer': ds_course + web_course + ai_course,
        'DotNet Developer': web_course,
        'Automation Testing': web_course,
        'Testing': web_course,

        # --- Data & AI ---
        'Data Science': ds_course + ai_course + data_eng_course,
        'Machine Learning Engineer': ai_course + ds_course,
        'AI Engineer': ai_course + ds_course,
        'Artificial Intelligence': ai_course + ds_course,
        'Business Analyst': ds_course + data_eng_course,

        # --- Web & Design ---
        'Web Designing': web_course + uiux_course,
        'Frontend Developer': web_course + uiux_course,
        'Full Stack Developer': web_course + cloud_course,
        'UI/UX Designer': uiux_course,

        # --- Cloud & DevOps ---
        'DevOps Engineer': cloud_course,
        'Cloud Engineer': cloud_course,
        'Site Reliability Engineer': cloud_course,

        # --- Cybersecurity ---
        'Network Security Engineer': cyber_course,
        'Cybersecurity Analyst': cyber_course,
        'Ethical Hacker': cyber_course,

        # --- Database & Big Data ---
        'Database': data_eng_course,
        'Hadoop': data_eng_course,
        'ETL Developer': data_eng_course,
        'Data Engineer': data_eng_course,

        # --- Blockchain & Web3 ---
        'Blockchain': blockchain_course,
        'Web3 Developer': blockchain_course,
        'Smart Contract Developer': blockchain_course,

        # --- Others / General Fields ---
        'HR': [],
        'Operations Manager': [],
        'SAP Developer': cloud_course,
        'Mechanical Engineer': [],
        'Civil Engineer': [],
        'Electrical Engineering': [],
        'Sales': [],
        'Arts': uiux_course,
        'Health and fitness': [],
        'Advocate': [],
        'PMO': [],
    }

    # Fallback recommendation (in case category not found)
    fallback_courses = ds_course + web_course + ai_course
    return category_course_map.get(predicted_category, fallback_courses)


import re

def filter_jobs_by_category(jobs, predicted_category):
    """
    Filter and rank jobs based on how relevant they are to the predicted career category.
    Uses weighted keyword matching (core vs related), fuzzy matching, and adaptive fallback.
    """

    if not predicted_category or not jobs:
        return jobs

    # ========== SMART FUZZY MATCHER ==========
    def keyword_in_text(keyword, text):
        """Smart matching for plural, hyphen, spacing variations"""
        pattern = r'\b' + re.escape(keyword).replace(r'\-', '[-\s]?') + r's?\b'
        return re.search(pattern, text, re.IGNORECASE)

    # ========== CATEGORY KEYWORDS ==========
    category_keywords = {
        # --- Core Developer Roles ---
        'Java Developer': {
            'core': ['java', 'spring', 'jvm', 'kotlin'],
            'related': ['backend', 'software', 'developer', 'engineer']
        },
        'Python Developer': {
            'core': ['python', 'django', 'flask'],
            'related': ['backend', 'software', 'developer', 'ai', 'ml']
        },
        'Web Designing': {
            'core': ['web', 'frontend', 'ui', 'ux', 'html', 'css'],
            'related': ['react', 'angular', 'vue', 'javascript', 'designer']
        },
        'Full Stack Developer': {
            'core': ['full stack', 'mern', 'mean', 'frontend', 'backend'],
            'related': ['react', 'node', 'express', 'django', 'api']
        },
        'Android Developer': {
            'core': ['android', 'kotlin', 'java', 'mobile'],
            'related': ['flutter', 'compose']
        },
        'iOS Developer': {
            'core': ['ios', 'swift', 'swiftui', 'xcode'],
            'related': ['mobile', 'app', 'developer']
        },

        # --- Data & AI ---
        'Data Science': {
            'core': ['data', 'scientist', 'analytics', 'analysis'],
            'related': ['machine learning', 'ml', 'ai', 'insight', 'python', 'sql']
        },
        'Machine Learning Engineer': {
            'core': ['machine learning', 'ml', 'ai', 'neural'],
            'related': ['pytorch', 'tensorflow', 'deep learning']
        },
        'AI Engineer': {
            'core': ['ai', 'artificial intelligence', 'ml', 'deep learning'],
            'related': ['llm', 'nlp', 'vision', 'transformer']
        },
        'Data Engineer': {
            'core': ['data engineer', 'pipeline', 'etl', 'big data'],
            'related': ['airflow', 'spark', 'hadoop', 'aws glue', 'kafka']
        },
        'Business Analyst': {
            'core': ['business analyst', 'data', 'requirements', 'insights'],
            'related': ['excel', 'tableau', 'power bi']
        },

        # --- Cloud & DevOps ---
        'DevOps Engineer': {
            'core': ['devops', 'ci/cd', 'docker', 'kubernetes'],
            'related': ['aws', 'azure', 'gcp', 'infrastructure', 'terraform']
        },
        'Cloud Engineer': {
            'core': ['cloud', 'aws', 'azure', 'gcp', 'infrastructure'],
            'related': ['devops', 'serverless', 'kubernetes', 'docker']
        },
        'Site Reliability Engineer': {
            'core': ['sre', 'reliability', 'monitoring'],
            'related': ['devops', 'cloud', 'automation']
        },

        # --- Cybersecurity ---
        'Network Security Engineer': {
            'core': ['network', 'security', 'cyber'],
            'related': ['infosec', 'pentesting', 'firewall', 'ethical hacking']
        },
        'Cybersecurity Analyst': {
            'core': ['cybersecurity', 'security analyst', 'threat', 'incident'],
            'related': ['vulnerability', 'forensics', 'malware', 'siem']
        },
        'Ethical Hacker': {
            'core': ['ethical hacker', 'pentest', 'penetration testing'],
            'related': ['bug bounty', 'offensive security', 'owasp']
        },

        # --- Blockchain & Web3 ---
        'Blockchain Developer': {
            'core': ['blockchain', 'web3', 'solidity', 'crypto'],
            'related': ['ethereum', 'smart contract', 'defi']
        },
        'Web3 Developer': {
            'core': ['web3', 'blockchain', 'solidity'],
            'related': ['dapp', 'nft', 'crypto']
        },

        # --- UI/UX & Creative ---
        'UI/UX Designer': {
            'core': ['ui', 'ux', 'figma', 'design'],
            'related': ['prototype', 'wireframe', 'adobe', 'user research']
        },

        # --- Other Tech Roles ---
        'Database': {
            'core': ['database', 'dba', 'sql'],
            'related': ['oracle', 'mongodb', 'mysql', 'postgresql']
        },
        'Testing': {
            'core': ['testing', 'qa', 'quality', 'automation'],
            'related': ['selenium', 'software', 'engineer']
        },
        'SAP Developer': {
            'core': ['sap', 'erp'],
            'related': ['developer', 'abap']
        },
        'Operations Manager': {
            'core': ['operations', 'manager'],
            'related': ['project', 'business', 'process']
        },
    }

    # ========== GET CATEGORY KEYWORDS ==========
    keyword_set = category_keywords.get(predicted_category, {})
    core_keywords = keyword_set.get('core', [])
    related_keywords = keyword_set.get('related', [])

    if not core_keywords and not related_keywords:
        return jobs  # no filtering if unknown category

    # ========== FILTER & SCORE JOBS ==========
    scored_jobs = []

    for job in jobs:
        title = (job.get('title', '') or '').lower().replace('-', ' ')
        description = (job.get('description', '') or '').lower().replace('-', ' ')
        company = (job.get('company', '') or '').lower()
        tags = ' '.join(job.get('tags', [])).lower()
        job_text = f"{title} {description} {company} {tags}"

        title_score, body_score = 0, 0

        # --- Score titles ---
        for keyword in core_keywords:
            if keyword_in_text(keyword, title):
                title_score += 5
        for keyword in related_keywords:
            if keyword_in_text(keyword, title):
                title_score += 2

        # --- Score description, company, tags ---
        for keyword in core_keywords:
            if keyword_in_text(keyword, job_text):
                body_score += 3
        for keyword in related_keywords:
            if keyword_in_text(keyword, job_text):
                body_score += 1

        total_score = title_score + body_score

        has_core = any(keyword_in_text(kw, job_text) for kw in core_keywords)
        has_strong_title = title_score >= 3

        if has_core or has_strong_title or total_score >= 4:
            scored_jobs.append((job, total_score))

    # ========== SORT & FALLBACK ==========
    scored_jobs.sort(key=lambda x: x[1], reverse=True)
    filtered_jobs = [job for job, score in scored_jobs]

    # If filtering removes too many jobs, fallback to original list
    if len(filtered_jobs) < max(3, len(jobs) * 0.2):
        return jobs

    return filtered_jobs if filtered_jobs else jobs


# -----------------------------
# Application Setup
# -----------------------------

def initialize_app():
    """Initialize the Streamlit application"""
    # Initialize page state if it doesn't exist
    if 'page' not in st.session_state:
        st.session_state.page = "analyzer"  # Skip landing page, go directly to analyzer
    # Set page config with theme first
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon=Config.APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Apply custom CSS for dark theme
    st.markdown("""
    <style>
        :root {
            --primary: #6366F1;
            --primary-light: #818CF8;
            --primary-dark: #4F46E5;
            --secondary: #8B5CF6;
            --accent: #10B981;
            --dark-bg: #0A0E27;
            --dark-surface: #141A35;
            --dark-card: #1A1F3A;
            --dark-border: #2D3748;
            --text-primary: #F8FAFC;
            --text-secondary: #9CA3AF;
            --gradient-primary: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            --gradient-secondary: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
            --glow-primary: 0 0 20px rgba(99, 102, 241, 0.3);
            --glow-secondary: 0 0 30px rgba(139, 92, 246, 0.4);
        }
        
        /* Base styles with animations */
        .stApp {
            background: linear-gradient(135deg, #0A0E27 0%, #0F1532 50%, #141A35 100%);
            color: var(--text-primary);
            background-attachment: fixed;
        }
        
        /* Sidebar */
        .css-1d391kg, .e1fqkh3o3 {
            background: linear-gradient(180deg, #141A35 0%, #1A1F3A 100%) !important;
            border-right: 1px solid rgba(99, 102, 241, 0.1) !important;
        }
        
        /* File uploader */
        .stFileUploader > div > div > div > button {
            background: var(--primary);
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            transition: all 0.2s ease;
        }
        
        .stFileUploader > div > div > div > button:hover {
            background: var(--primary-light);
            transform: translateY(-1px);
        }
        
        /* File uploader text */
        .stFileUploader > div > div > div > div > div > div {
            color: #E2E8F0 !important;  /* Lighter text color for better visibility */
            background-color: #1E293B;   /* Dark background for the text area */
            padding: 8px 12px;          /* Add some padding around the text */
            border-radius: 4px;          /* Rounded corners */
            border: 1px solid #475569;   /* Subtle border */
            margin-top: 4px;            /* Add some space above the text */
        }
        
        .stFileUploader > div > div > div > div > div > div::before {
            color: #E2E8F0 !important;  /* Lighter color for the icon */
            margin-right: 8px;          /* Add space between icon and text */
        }
        
        .stFileUploader > div > div > div > div > div > div::after {
            color: #E2E8F0 !important;  /* Lighter color for any after content */
        }
        
        /* Make the file name more visible */
        .stFileUploader > div > div > div > div > div > div > span {
            color: #E2E8F0 !important;
            font-weight: 500;           /* Slightly bolder text */
        }
        
        /* Buttons - Professional Styling */
        .stButton > button {
            background: var(--gradient-primary);
            color: white;
            border: 2px solid transparent;
            border-radius: 10px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .stButton > button:hover {
            background: var(--gradient-secondary);
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4), var(--glow-secondary);
            transform: translateY(-2px);
        }
        
        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
        }
        
        /* Input fields - Enhanced */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: rgba(26, 31, 58, 0.8);
            color: var(--text-primary);
            border: 2px solid rgba(99, 102, 241, 0.2);
            border-radius: 10px;
            transition: all 0.3s ease;
            padding: 12px 16px !important;
            font-size: 14px;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #6366F1;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.3), inset 0 0 10px rgba(99, 102, 241, 0.1);
            background-color: rgba(26, 31, 58, 1);
        }
        
        /* Select boxes - Enhanced */
        .stSelectbox > div > div > div {
            background-color: rgba(26, 31, 58, 0.8);
            color: var(--text-primary);
            border: 2px solid rgba(99, 102, 241, 0.2);
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div > div:hover {
            border-color: #6366F1;
            background-color: rgba(26, 31, 58, 1);
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Validate configuration
    config_status = Config.validate_config()
    if not config_status['valid']:
        st.error("Configuration issues found:")
        for issue in config_status['issues']:
            st.error(f"- {issue}")
        st.stop()
    
    # Show warnings if any
    if config_status.get('warnings'):
        for warning in config_status['warnings']:
            st.warning(f"⚠️ {warning}")
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "light"
    
    # Ensure NLTK data only once per session
    if not st.session_state.get("nltk_ready"):
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        st.session_state["nltk_ready"] = True
    
    # Apply styles
    StyleManager.apply_global_styles()
    StyleManager.apply_theme_styles(st.session_state.theme_mode)
    # Professional sidebar chat styles
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
        
        .sb-chip:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(79, 70, 229, 0.3);
        }}
        
        .msg-wrap {{
            max-height: 60vh; 
            overflow-y: auto; 
            padding-right: 6px;
            margin: 16px 0;
        }}
        
        .msg {{
            margin: 10px 0; 
            padding: 12px 16px; 
            border-radius: 16px; 
            line-height: 1.4;
            font-size: 0.875rem;
            transition: all 0.2s ease;
        }}
        
        .msg:hover {{
            transform: translateY(-1px);
        }}
        
        .msg-user {{
            background: {StyleManager.COLORS['primary_gradient']}; 
            color: white;
            border: none;
            margin-left: 20px;
            border-bottom-right-radius: 6px;
        }}
        
        .msg-assist {{
            background: rgba(255, 255, 255, 0.08); 
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: inherit;
            margin-right: 20px;
            border-bottom-left-radius: 6px;
            backdrop-filter: blur(8px);
        }}
        
        .msg-role {{
            font-size: 0.625rem; 
            opacity: 0.7; 
            margin-bottom: 4px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        /* Sidebar scrollbar */
        .msg-wrap::-webkit-scrollbar {{
            width: 6px;
        }}
        
        .msg-wrap::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 3px;
        }}
        
        .msg-wrap::-webkit-scrollbar-thumb {{
            background: {StyleManager.COLORS['primary_gradient']};
            border-radius: 3px;
        }}
        
        .msg-wrap::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, {StyleManager.COLORS['primary_light']} 0%, {StyleManager.COLORS['primary_dark']} 100%);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

@st.cache_resource(show_spinner=False)
def get_resume_parser():
    """Get cached resume parser instance"""
    return ResumeParser()

@st.cache_data
def _load_nevera_font():
    """Load and encode Nevera font as base64"""
    try:
        font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nevera_font', 'Nevera-Regular.otf')
        if not os.path.exists(font_path):
            return ""
        with open(font_path, 'rb') as f:
            font_bytes = f.read()
        encoded = base64.b64encode(font_bytes).decode('utf-8')
        return encoded
    except Exception as e:
        return ""

def display_header():
    """Display professional application header with ultra-modern design"""
    # Apply animations
    st.markdown(StyleManager.get_animation_styles(), unsafe_allow_html=True)
    
    # Apply default light theme
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'light'
        StyleManager.apply_theme_styles('light')
    
    # Load font inline
    font_b64 = _load_nevera_font()
    
    # Ultra-professional header with modern design  
    st.markdown(f"""
    <style>
    /* ---------------- CUSTOM FONT ---------------- */
    @font-face {{
        font-family: 'Nevera';
        src: url('data:application/x-font-opentype;base64,{font_b64}') format('opentype'),
             url('data:font/otf;base64,{font_b64}') format('opentype');
        font-weight: 400;
        font-style: normal;
        font-display: swap;
    }}
    
    /* ---------------- HERO SECTION ---------------- */
    .hero-section {{
        position: relative;
        background: radial-gradient(120% 160% at 50% 10%, #0e132a 20%, #0b1028 100%);
        padding: 100px 20px 120px;
        text-align: center;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 40px rgba(0,0,0,0.25);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .hero-section:hover {{
        transform: scale(1.005);
        box-shadow: 0 12px 45px rgba(0,0,0,0.3);
    }}

    /* Subtle background animation with moving gradient */
    .hero-section::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(120deg, rgba(124,58,237,0.1), rgba(45,212,191,0.1), rgba(124,58,237,0.1), rgba(45,212,191,0.1));
        background-size: 200% 200%;
        animation: moveGradient 10s ease-in-out infinite alternate;
        z-index: 0;
    }}

    @keyframes moveGradient {{
        0%% {{ background-position: 0% 50%; }}
        100%% {{ background-position: 100% 50%; }}
    }}

    /* Glow halo */
    .hero-section::after {{
        content: "";
        position: absolute;
        top: -150px;
        left: 50%;
        transform: translateX(-50%);
        width: 1000px;
        height: 1000px;
        background: radial-gradient(circle at 50% 50%, rgba(56, 189, 248, 0.1), rgba(99, 102, 241, 0.05) 70%, transparent 100%);
        filter: blur(120px);
        z-index: 0;
        animation: pulseGlow 8s ease-in-out infinite alternate;
    }}

    @keyframes pulseGlow {{
        0%% {{ opacity: 0.8; transform: translateX(-50%) scale(1); }}
        100%% {{ opacity: 1; transform: translateX(-50%) scale(1.08); }}
    }}

    /* ============ UNIFIED ANIMATIONS ============ */
    /* Smooth fade-up animation with cubic-bezier easing */
    @keyframes fadeUp {{
        0%% {{ opacity: 0; transform: translateY(40px); }}
        100%% {{ opacity: 1; transform: translateY(0); }}
    }}

    /* ---------------- TEXT STYLING ---------------- */
    .hero-badge {{
        display: inline-block;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.3);
        box-shadow: inset 0 0 10px rgba(255,255,255,0.05);
        backdrop-filter: blur(15px);
        color: #a5b4fc;
        padding: 8px 20px;
        border-radius: 50px;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 28px;
        letter-spacing: 0.5px;
        text-shadow: 0 0 10px rgba(165,180,252,0.3);
        animation: fadeUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        z-index: 2;
    }}
    
    .hero-branding {{
        font-family: 'Nevera', 'Helvetica Neue', Arial, sans-serif !important;
        font-size: 5.5rem;
        font-weight: 400;
        color: #fff;
        margin-bottom: 25px;
        margin-top: 20px;
        letter-spacing: 0.18em;
        animation: fadeUp 1s cubic-bezier(0.4, 0, 0.2, 1), gradientFlow 6s ease-in-out infinite alternate;
        position: relative;
        z-index: 2;
        text-transform: uppercase;
        font-feature-settings: 'kern' 1;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        background: linear-gradient(100deg, #8b5cf6, #2dd4bf, #38bdf8, #8b5cf6);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    @keyframes gradientFlow {{
        0%% {{ background-position: 0% 50%; }}
        100%% {{ background-position: 100% 50%; }}
    }}

    .hero-title {{
        font-family: 'Inter', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 20px;
        line-height: 1.2;
        letter-spacing: -0.02em;
        animation: fadeUp 1.1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        z-index: 2;
    }}

    .hero-title span {{
        color: #2cb67d;
        background: linear-gradient(135deg, #7f5af0, #2cb67d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .hero-desc {{
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        color: #94a3b8;
        max-width: 700px;
        margin: 0 auto 30px;
        line-height: 1.7;
        letter-spacing: 0.01em;
        padding: 0 10px;
        text-align: center;
        position: relative;
        z-index: 2;
    }}

    /* ---------------- CTA BUTTON ---------------- */
    .hero-cta {{
        text-align: center;
        margin-top: 32px;
    }}

    .cta-button {{
        display: inline-block;
        margin-top: 32px;
        padding: 14px 36px;
        background: linear-gradient(135deg, #6366f1, #14b8a6);
        border: none;
        border-radius: 50px;
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        text-decoration: none;
        box-shadow: 0 8px 20px rgba(99,102,241,0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        font-size: 1.05rem;
        letter-spacing: 0.02em;
        animation: fadeUp 1.2s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .cta-button::before {{
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }}
    
    .cta-button:hover::before {{
        left: 100%;
    }}

    .cta-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(99,102,241,0.5);
    }}
    
    .cta-button:active {{
        transform: translateY(0px);
        box-shadow: 0 4px 15px rgba(99,102,241,0.4);
    }}

    /* Scroll target for upload section */
    #upload-section {{
        scroll-margin-top: 20px;
    }}

    /* ---------------- RESPONSIVE DESIGN ---------------- */
    @media (max-width: 1024px) {{
        .hero-section {{ padding: 80px 20px 100px; }}
        .hero-branding {{ font-size: 4rem; }}
        .hero-title {{ font-size: 2.1rem; line-height: 1.2; }}
        .hero-desc {{ font-size: 1rem; max-width: 600px; line-height: 1.6; }}
        .hero-badge {{ font-size: 0.85rem; }}
        .cta-button {{ font-size: 1rem; padding: 12px 32px; }}
    }}

    @media (max-width: 768px) {{
        .hero-section {{ padding: 60px 16px 80px; }}
        .hero-branding {{ font-size: 3rem; letter-spacing: 0.12em; }}
        .hero-title {{ font-size: 1.7rem; line-height: 1.25; }}
        .hero-desc {{ font-size: 0.95rem; max-width: 100%; padding: 0 10px; line-height: 1.6; }}
        .hero-badge {{ font-size: 0.8rem; padding: 6px 16px; }}
        .cta-button {{ font-size: 0.95rem; padding: 12px 28px; margin-top: 24px; }}
    }}

    @media (max-width: 480px) {{
        .hero-section {{ padding: 50px 12px 70px; }}
        .hero-branding {{ font-size: 2.2rem; }}
        .hero-title {{ font-size: 1.6rem; line-height: 1.3; }}
        .hero-desc {{ font-size: 0.9rem; line-height: 1.6; }}
        .hero-badge {{ font-size: 0.75rem; padding: 5px 14px; }}
    }}
    </style>

    <!-- HERO SECTION -->
    <div class="hero-section">
        <div class="hero-badge">⚡ AI-Powered Internship Matching</div>
        <div class="hero-branding">INTERNHUNT</div>
        <h1 class="hero-title">Find Internships That <span>Fit You</span></h1>
        <div class="hero-cta">
            <a href="#upload-section" class="cta-button">Upload Resume</a>
        </div>
    </div>
""", unsafe_allow_html=True)


def get_table_download_link(df, filename, text):
    """Generate download link for dataframe"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def show_pdf(file_path):
    """Display PDF in Streamlit"""
    if not os.path.exists(file_path):
        st.error("PDF file not found.")
        return
    
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error displaying PDF: {e}")

def categorize_skills(skills):
    """Categorize skills into specific sections (languages, frontend, backend, libraries, etc.)."""
    categories = {
        "Languages": [],
        "Frontend": [],
        "Backend": [],
        "Libraries / Data-ML": [],
        "Databases": [],
        "Cloud / DevOps": [],
        "Mobile": [],
        "Tools / Platforms": [],
        "Embedded / Hardware": [],
        "Concepts": [],
        "Soft Skills": [],
        "Other": []
    }

    # Normalization aliases
    aliases = {
        'reactjs': 'react', 'nextjs': 'next.js', 'nodejs': 'node.js', 'postgres': 'postgresql',
        'ci cd': 'ci/cd', 'ci-cd': 'ci/cd', 'bs4': 'beautifulsoup', 'huggingface': 'hugging face',
        'redux toolkit': 'redux', 'tailwindcss': 'tailwind', 'postgre': 'postgresql',
        'google colaboratory': 'google colab', 'google-colab': 'google colab', 'visual studio code': 'vs code'
    }

    langs = {
        'python','java','javascript','typescript','go','rust','c','c++','c#','kotlin','swift','ruby','php','r','scala','matlab'
    }
    frontend = {
        'html','html5','css','css3','react','next.js','angular','vue','svelte','redux','tailwind','bootstrap','sass','less','vite','webpack','babel'
    }
    backend = {
        'node.js','express','django','flask','fastapi','spring','spring boot','laravel','rails','graphql','grpc','rest','openapi','swagger'
    }
    libs = {
        'numpy','pandas','scikit-learn','sklearn','matplotlib','seaborn','plotly','tensorflow','keras','pytorch','opencv','xgboost','lightgbm','transformers','hugging face','langchain','yolo','pyspark','spark','nltk','spacy','streamlit'
    }
    dbs = {'sql','mysql','postgresql','sqlite','mongodb','redis','elasticsearch'}
    devops = {'aws','gcp','azure','docker','kubernetes','terraform','git','github','gitlab','github actions','gitlab ci','ci/cd','linux','bash','shell','nginx'}
    mobile = {'android','ios','react native','swiftui','flutter','firebase','supabase'}
    tools = {'postman','selenium','beautifulsoup','power bi','tableau','excel','airflow','hive','hadoop','looker','superset','colab','google colab','vscode','vs code','powerpoint','ms powerpoint','api integration','jupyter'}
    embedded = {'verilog','vhdl','systemverilog','fpga','pcb design','circuit design','embedded systems','arm','arm cortex-m','stm32','esp32','raspberry pi','msp430','pic','arduino'}
    soft = {'communication','leadership','teamwork','collaboration','problem solving','time management','adaptability','critical thinking'}
    concepts = {'data analysis','operating systems','os','networking fundamentals'}

    def norm(s):
        s0 = (s or '').strip()
        if not s0:
            return None
        low = s0.lower()
        low = aliases.get(low, low)
        # unify minor variants
        low = low.replace('react.js','react').replace('next js','next.js').replace('node js','node.js')
        return low, s0  # return original-cased too

    for s in skills:
        res = norm(s)
        if not res:
            continue
        low, orig = res
        if low in langs:
            categories['Languages'].append(orig)
        elif low in frontend:
            categories['Frontend'].append(orig)
        elif low in backend:
            categories['Backend'].append(orig)
        elif low in libs:
            categories['Libraries / Data-ML'].append(orig)
        elif low in dbs:
            categories['Databases'].append(orig)
        elif low in devops:
            categories['Cloud / DevOps'].append(orig)
        elif low in mobile:
            categories['Mobile'].append(orig)
        elif low in tools:
            categories['Tools / Platforms'].append(orig)
        elif low in embedded:
            categories['Embedded / Hardware'].append(orig)
        elif low in soft:
            categories['Soft Skills'].append(orig)
        elif low in concepts:
            categories['Concepts'].append(orig)
        else:
            categories['Other'].append(orig)

    # Drop empty categories and de-duplicate while preserving order
    out = {}
    for k, v in categories.items():
        if not v:
            continue
        seen = set()
        ordered = []
        for item in v:
            if item not in seen:
                seen.add(item)
                ordered.append(item)
        out[k] = ordered
    return out

def display_skills(categorized_skills):
    """Display categorized skills with professional styling"""
    st.markdown(StyleManager.get_skills_styles(), unsafe_allow_html=True)
    
    st.markdown("""
        <div class="skills-header animate-fade-in">
            <div class="skills-header-icon">🛠️</div>
            <h2 class="skills-header-text">SKILLS EXTRACTED</h2>
        </div>
    """, unsafe_allow_html=True)
    
    category_icons = {
        "Languages": "🧠",
        "Frontend": "🎨",
        "Backend": "🧩",
        "Libraries / Data-ML": "📚",
        "Databases": "🗄️",
        "Cloud / DevOps": "☁️",
        "Mobile": "📱",
        "Tools / Platforms": "🧰",
        "Embedded / Hardware": "🔌",
        "Concepts": "🧩",
        "Soft Skills": "🤝",
        "Other": "🔧"
    }
    
    css_class_map = {
        "Languages": "tech-skill",
        "Frontend": "design-skill",
        "Backend": "tech-skill",
        "Libraries / Data-ML": "data-skill",
        "Databases": "data-skill",
        "Cloud / DevOps": "tech-skill",
        "Mobile": "tech-skill",
        "Tools / Platforms": "business-skill",
        "Embedded / Hardware": "hardware-skill",
        "Concepts": "business-skill",
        "Soft Skills": "soft-skill",
        "Other": "other-skill"
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

def _fetch_all_jobs(skills, user_location):
    """Fetch and merge Jooble + scraper jobs into a common schema and deduplicate by URL."""
    jooble_jobs = JobAPIService.fetch_jobs_from_jooble(skills, user_location) or []
    scraped_jobs = scrape_all(skills, user_location) or []

    def map_jooble(j):
        return {
            "title": j.get("title", ""),
            "company": j.get("company", ""),
            "location": j.get("location", "") or "Remote",
            "tags": [],
            "description": j.get("snippet", ""),
            "url": j.get("link", "#"),
            "source": "jooble",
        }

    def map_scraper(j):
        return {
            "title": j.get("title", ""),
            "company": j.get("company", ""),
            "location": j.get("location", "") or "Remote",
            "tags": j.get("tags", []),
            "description": j.get("description", ""),
            "url": j.get("url", "#"),
            "source": j.get("source", "scraper"),
        }

    merged = [map_jooble(j) for j in jooble_jobs] + [map_scraper(j) for j in scraped_jobs]

    # Deduplicate by URL
    seen = set()
    unique = []
    for j in merged:
        u = j.get("url")
        if not u or u in seen:
            continue
        seen.add(u)
        unique.append(j)
    return unique

def _filter_jobs(jobs, query, source):
    """Client-side filter by source and free-text query over multiple fields."""
    q = (query or "").strip().lower()
    s = (source or "All").lower()
    def keep(j):
        js = j.get("source", "").lower()
        if s == "jooble":
            if js != "jooble":
                return False
        elif s == "scrapers":
            # Treat any non-jooble as a scraper
            if js == "jooble":
                return False
        # else: s == all -> no source filter
        if not q:
            return True
        # Prefer matching location first; many scrapers use 'Remote'
        loc = (j.get("location", "") or "").lower()
        if q in loc:
            return True
        # Consider 'remote' a match if user typed something like 'remote'
        if q in ("remote", "wfh", "work from home") and ("remote" in loc or loc == ""):
            return True
        # Otherwise, perform a soft match against title/company/tags/description
        blob = " ".join([
            j.get("title", ""),
            j.get("company", ""),
            " ".join(j.get("tags", [])),
            j.get("description", ""),
        ]).lower()
        return q in blob
    return [j for j in (jobs or []) if keep(j)]

def display_job_recommendations_dual(skills_list, keywords_text: str, location_text: str, predicted_category=None):
    """Display two sections: Jooble jobs and Internshala internships, fetched concurrently."""
    from concurrent.futures import ThreadPoolExecutor
    st.markdown(StyleManager.get_job_listing_styles(), unsafe_allow_html=True)
    st.markdown(StyleManager.get_animation_styles(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="animated-header" style="
            background-color: #111827;
            padding: 1.2rem;
            border-radius: 8px;
            margin-top: 2rem;
            margin-bottom: 1rem;
        ">
            <h1 style='color: #ffffff; margin: 0;'>💼 Job Recommendations</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Build query skills: manual text -> split by commas; else resume skills
    manual = (keywords_text or "").strip()
    if manual:
        query_skills = [s.strip() for s in manual.split(',') if s.strip()]
    else:
        query_skills = [s for s in (skills_list or []) if s]

    # Build a simple keyword query string for Internshala
    # If we have a predicted category, use category-specific keywords
    if predicted_category:
        category_search_terms = {
            'Java Developer': 'java developer',
            'Python Developer': 'python developer',
            'Data Science': 'data analyst',  # Most relevant for internships
            'Web Designing': 'web design',
            'DevOps Engineer': 'devops',
            'HR': 'hr',
            'Testing': 'software testing',
            'Database': 'database',
            'Blockchain': 'blockchain',
            'Operations Manager': 'operations',
            'SAP Developer': 'sap',
            'Mechanical Engineer': 'mechanical',
            'Civil Engineer': 'civil',
            'Electrical Engineering': 'electrical',
            'Network Security Engineer': 'cyber security',
        }
        query_str = category_search_terms.get(predicted_category, ", ".join(query_skills[:3]))
    else:
        query_str = ", ".join(query_skills)

    # Jooble-specific location input (placed before fetch to avoid unbound errors)
    jooble_loc = st.text_input("Jooble Location", value=(location_text or ""), key="jooble_location_input")
    jooble_fetch = st.button("Search Jooble", key="jooble_search_btn")

    # Show what we're searching for (helps with debugging)
    if predicted_category:
        st.info(f"🎯 Searching for **{predicted_category}** internships using keywords: '{query_str}'")
    
    # Fetch both sources concurrently (Jooble + Internshala scraper)
    with st.spinner("Fetching opportunities..."):
        with ThreadPoolExecutor(max_workers=2) as ex:
            f1 = ex.submit(JobAPIService.fetch_jobs_from_jooble, query_skills[:5], jooble_loc or "")
            f2 = ex.submit(scrape_internshala_by_keywords, query_str or "", (location_text or "India"))
            jooble_jobs = f1.result() or []
            internshala_jobs = f2.result() or []
    
    # Apply ML-based category filtering if available
    if predicted_category:
        orig_jooble = len(jooble_jobs)
        orig_intern = len(internshala_jobs)
        jooble_jobs = filter_jobs_by_category(jooble_jobs, predicted_category)
        internshala_jobs = filter_jobs_by_category(internshala_jobs, predicted_category)
        st.success(f"✅ Filtered jobs: Jooble {orig_jooble} → {len(jooble_jobs)} | Internshala {orig_intern} → {len(internshala_jobs)}")

    # If nothing from keywords page, try generic scraper with skills
    if not internshala_jobs:
        try:
            internshala_jobs = scrape_internshala(query_skills, location_text) or []
        except Exception:
            internshala_jobs = []

    # Final relax: latest internships (no filters, India)
    if not internshala_jobs:
        try:
            internshala_jobs = scrape_internshala([], "India") or scrape_internshala([], "") or []
        except Exception:
            internshala_jobs = []

    # Section: Jooble
    st.markdown(
        """
        <div class="animated-header" style="
            background-color: #1e1e1e;
            padding: 0.8rem;
            border-left: 6px solid #60a5fa;
            border-radius: 6px;
            margin-top: 1.2rem;
            margin-bottom: 0.6rem;
        ">
            <h2 style='color: #ffffff; margin: 0;'>Job Recommendations from Jooble (Global)</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if jooble_jobs:
        for i, job in enumerate(jooble_jobs[:10]):
            display_job_card(job, "jooble")
            if i < min(10, len(jooble_jobs)) - 1:
                st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    else:
        st.info("No opportunities found based on your skills.")

    # Section: Internshala
    st.markdown(
        """
        <div class="animated-header" style="
            background-color: #1e1e1e;
            padding: 0.8rem;
            border-left: 6px solid #34d399;
            border-radius: 6px;
            margin-top: 1.6rem;
            margin-bottom: 0.6rem;
        ">
            <h2 style='color: #ffffff; margin: 0;'>🇮🇳 Internships from Internshala (India)</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Separate Internshala keyword + location inputs
    c_ik, c_il, c_ib = st.columns([3, 2, 1])
    with c_ik:
        intern_kw = st.text_input("Internshala Keywords", value=(query_str or ""), key="intern_kw_input")
    with c_il:
        intern_loc = st.text_input("Internshala Location", value=(location_text or "India"), key="intern_loc_input")
    with c_ib:
        intern_btn = st.button("Search Internshala", key="intern_search_btn")

    # If user changed inputs, refresh Internshala results accordingly
    def _filter_intern_relevance(items, kw_text: str, resume_skills: list):
        # Build a keyword set from user-entered keywords + resume skills
        def norm_terms(text: str) -> list:
            import re
            toks = [t.strip().lower() for t in re.split(r"[^a-z0-9\+\.#]+", text or "") if t.strip()]
            return toks
        kws = set(norm_terms(kw_text))
        for s in (resume_skills or [])[:15]:
            if isinstance(s, str):
                kws.update(norm_terms(s))
        if not items or not kws:
            return items
        keep = []
        for j in items:
            title = (j.get('title') or '').lower()
            desc = (j.get('description') or '').lower()
            comp = (j.get('company') or '').lower()
            loc = (j.get('location') or '').lower()
            blob = " ".join([title, comp, loc, desc])
            if any(k in title for k in kws) or any(k in desc for k in kws):
                keep.append(j)
        # If filtering removed everything, fall back to original list
        return keep or items

    def _enrich_internshala_descriptions(items, max_fetch: int = 6):
        try:
            import re
            import json
            import requests
            from bs4 import BeautifulSoup
        except Exception:
            return items
        out = []
        fetched = 0
        HEADERS_LOCAL = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml"
        }
        def clean(txt: str) -> str:
            t = re.sub(r"\s+", " ", (txt or "").strip())
            return t
        def looks_generic(t: str) -> bool:
            low = t.lower()
            return (
                "explore more internships" in low or
                "top locations" in low or
                "top categories" in low or
                low.startswith("find ") or
                (len(low) < 40)
            )
        def bullets_to_line(uls) -> str:
            bullets = []
            for ul in uls:
                for li in ul.select('li'):
                    s = clean(li.get_text(" ", strip=True))
                    if s and len(s) > 8:
                        bullets.append(s)
                    if len(bullets) >= 2:
                        break
                if len(bullets) >= 2:
                    break
            return " • ".join(bullets)
        def extract_role_snippet(soup: 'BeautifulSoup') -> str:
            # Prefer bullets near headings like "About the internship", "Role Overview", "Responsibilities"
            heading_patterns = ["about the internship", "role overview", "responsibilities", "what you will do"]
            for h in soup.select('h1, h2, h3, h4, strong, b'):
                text = h.get_text(" ", strip=True).lower()
                if any(p in text for p in heading_patterns):
                    # look in next siblings for ul/ol
                    sib = h.find_next_sibling()
                    uls = []
                    while sib and len(uls) == 0 and sib.name not in ('h1','h2','h3','h4'):
                        if sib.name in ('ul','ol'):
                            uls.append(sib)
                            break
                        uls.extend(sib.select('ul,ol'))
                        sib = sib.find_next_sibling()
                    if uls:
                        line = bullets_to_line(uls)
                        if line and not looks_generic(line):
                            return line
            # Fallback: any bullets under known containers
            uls = soup.select('section#about ul, div#internship_about ul, div.internship_about ul, div.job-description ul, div#job-description ul, div#job-detail ul')
            line = bullets_to_line(uls)
            return line
        for j in items or []:
            if (not j.get('description')) and isinstance(j.get('url'), str) and j['url'].startswith("https://internshala.com/") and fetched < max_fetch:
                try:
                    r = requests.get(j['url'], headers=HEADERS_LOCAL, timeout=10)
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text, 'lxml')
                        text = None
                        # Try structured extraction first
                        line = extract_role_snippet(soup)
                        if line and not looks_generic(line):
                            text = line
                        # meta descriptions
                        if not text:
                            md = soup.select_one('meta[name="description"]')
                            if md and md.get('content'):
                                cand = clean(md['content'])
                                if cand and not looks_generic(cand):
                                    text = cand
                        if not text:
                            md = soup.select_one('meta[property="og:description"]')
                            if md and md.get('content'):
                                cand = clean(md['content'])
                                if cand and not looks_generic(cand):
                                    text = cand
                        # JSON-LD
                        if not text:
                            for s in soup.select('script[type="application/ld+json"]'):
                                try:
                                    data = json.loads(s.get_text(strip=True))
                                    def _pick(d):
                                        desc = d.get('description')
                                        if desc:
                                            cand = BeautifulSoup(desc, 'lxml').get_text(" ", strip=True)
                                            cand = clean(cand)
                                            if cand and not looks_generic(cand):
                                                return cand
                                    if isinstance(data, dict) and data.get('@type') in ("JobPosting","Internship"):
                                        cand = _pick(data)
                                        if cand:
                                            text = cand; break
                                    if isinstance(data, list):
                                        for d in data:
                                            if isinstance(d, dict) and d.get('@type') in ("JobPosting","Internship"):
                                                cand = _pick(d)
                                                if cand:
                                                    text = cand; break
                                        if text:
                                            break
                                except Exception:
                                    continue
                        # Narrow DOM fallback
                        if not text:
                            sel_list = [
                                'section#about', 'div#about_company', 'div#internship_about', 'div.internship_about',
                                'div#job-detail', 'div#job-description', 'div.job-description', 'div#jd', 'section#jd'
                            ]
                            for sel in sel_list:
                                el = soup.select_one(sel)
                                if el:
                                    cand = clean(el.get_text(" ", strip=True))
                                    if cand and not looks_generic(cand):
                                        text = cand
                                        break
                        if text:
                            j['description'] = (text[:200] + '...') if len(text) > 200 else text
                            fetched += 1
                except Exception:
                    pass
            out.append(j)
        return out

    if intern_btn and (intern_kw is not None or intern_loc is not None):
        try:
            internshala_jobs = scrape_internshala_by_keywords(intern_kw or "", intern_loc or "India") or []
            internshala_jobs = _filter_intern_relevance(internshala_jobs, intern_kw, skills_list)
        except Exception:
            internshala_jobs = internshala_jobs

    # Apply relevance filter and enrich summaries
    internshala_jobs = _filter_intern_relevance(internshala_jobs, intern_kw or query_str, skills_list)
    internshala_jobs = _enrich_internshala_descriptions(internshala_jobs)
    if internshala_jobs:
        for i, job in enumerate(internshala_jobs[:10]):
            display_job_card(job, "internshala")
            # If we have a relative link path, prefer the explicit Apply Here link format
            href = job.get('url', '#')
            if href:
                if href.startswith("https://internshala.com/"):
                    rel = href.replace("https://internshala.com", "")
                    st.markdown(f"[Apply Here](https://internshala.com{rel})", unsafe_allow_html=True)
                else:
                    st.markdown(f"[Apply Here]({href})", unsafe_allow_html=True)
            if i < min(10, len(internshala_jobs)) - 1:
                st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    else:
        st.info("No internships found for your skills in this region.")

def display_job_recommendations(skills, location):
    """Legacy API-only recommendations (kept for compatibility)."""
    st.markdown(StyleManager.get_job_listing_styles(), unsafe_allow_html=True)
    st.markdown(StyleManager.get_animation_styles(), unsafe_allow_html=True)
    
    st.markdown("""
        <div class="animated-header" style="
            background-color: #111827;
            padding: 1.2rem;
            border-radius: 8px;
            margin-top: 2rem;
            margin-bottom: 2rem;
        ">
            <h1 style='color: #ffffff; margin: 0;'>💼 Job Recommendations</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Jooble jobs
    st.markdown("""
        <div class="animated-header" style="
            background-color: #1e1e1e;
            padding: 0.8rem;
            border-left: 6px solid #60a5fa;
            border-radius: 6px;
            margin-top: 2rem;
            margin-bottom: 1rem;
        ">
            <h2 style='color: #ffffff; margin: 0;'>Job Recommendations from Jooble (Global)</h2>
        </div>
    """, unsafe_allow_html=True)
    
    jooble_jobs = JobAPIService.fetch_jobs_from_jooble(skills, location)
    
    if jooble_jobs:
        for i, job in enumerate(jooble_jobs[:10]):
            display_job_card(job, "jooble")
            if i < min(10, len(jooble_jobs)) - 1:
                st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    else:
        st.info("No opportunities found based on your skills.")

    # Internshala API (if configured)
    st.markdown("""
        <div class="animated-header" style="
            background-color: #1e1e1e;
            padding: 0.8rem;
            border-left: 6px solid #34d399;
            border-radius: 6px;
            margin-top: 1.6rem;
            margin-bottom: 0.6rem;
        ">
            <h2 style='color: #ffffff; margin: 0;'>🇮🇳 Internships from Internshala (India)</h2>
        </div>
    """, unsafe_allow_html=True)

    insh_raw = fetch_internshala_internships(", ".join([s for s in (skills or []) if s]), location or "India") or []
    if insh_raw:
        norm = []
        for it in insh_raw[:10]:
            link_path = it.get('link') or ''
            norm.append({
                "title": it.get('title') or it.get('profile') or 'Internship',
                "company": it.get('company') or it.get('company_name') or '',
                "location": it.get('location') or it.get('location_names') or 'India',
                "url": f"https://internshala.com{link_path}" if link_path.startswith('/') else (link_path or '#'),
                "description": it.get('description') or '',
                "source": "internshala",
                "_raw_link_path": link_path,
            })
        for i, job in enumerate(norm):
            display_job_card(job, "internshala")
            if job.get('_raw_link_path'):
                st.markdown(f"[Apply Here](https://internshala.com{job['_raw_link_path']})", unsafe_allow_html=True)
            if i < min(10, len(norm)) - 1:
                st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    else:
        st.info("No internships found matching your skills.")

def display_job_card(job, source):
    """Display individual job card (title, company, exact location, pay)."""
    pay = None
    duration = None
    if source == "adzuna":
        job_title = job.get("title", "No Title")
        company_name = job.get("company", {}).get("display_name", "Unknown Company")
        job_location = job.get("location", {}).get("display_name", "Location Not Available")
        job_link = job.get("redirect_url", "#")
        # Salary range if available
        smin = job.get("salary_min")
        smax = job.get("salary_max")
        if smin or smax:
            try:
                smin_i = int(float(smin)) if smin else None
                smax_i = int(float(smax)) if smax else None
                if smin_i and smax_i:
                    pay = f"₹ {smin_i:,} – {smax_i:,}"
                elif smin_i:
                    pay = f"₹ {smin_i:,}+"
                elif smax_i:
                    pay = f"Up to ₹ {smax_i:,}"
            except Exception:
                pay = None
    elif source == "jooble":  # jooble
        job_title = job.get("title", "No Title")
        company_name = job.get("company", "Unknown Company")
        job_location = job.get("location", "Location Not Available")
        job_link = job.get("link", "#")
        pay = job.get("salary") or job.get("compensation")
    elif source == "internshala":
        job_title = job.get("title", "Internship")
        company_name = job.get("company", "")
        job_location = job.get("location", "India")
        job_link = job.get("url", "#")
        pay = job.get("stipend") or job.get("salary")
        duration = job.get("duration")
    else:  # generic mapping for any future providers
        job_title = job.get("title", "No Title")
        company_name = job.get("company", "Unknown Company")
        job_location = job.get("location", "Remote")
        job_link = job.get("url", "#")
        pay = job.get("salary")
    
    st.markdown('<div class="job-listing">', unsafe_allow_html=True)
    source_name = (source or "").capitalize()
    badge = f"<span style='font-size:11px; padding:3px 8px; border:1px solid #374151; border-radius:999px; color:#9ca3af; background:rgba(255,255,255,0.04); margin-left:8px;'>{source_name}</span>"
    title_html = f"<strong>{job_title}</strong>" if source_name.lower() == "internshala" else job_title
    st.markdown(f"<div class=\"job-title\">🔹 {title_html} {badge}</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="job-info-container">', unsafe_allow_html=True)
    st.markdown('<div class="job-info">', unsafe_allow_html=True)
    
    # Company info
    company_val = f"<strong>{company_name}</strong>" if source_name.lower() == "internshala" else company_name
    st.markdown(f'''
    <div class="info-item">
        <span>🏢</span>
        <span class="info-label">Company:</span>
        <span>{company_val}</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # Location info
    loc_val = f"<strong>{job_location}</strong>" if source_name.lower() == "internshala" else job_location
    st.markdown(f'''
    <div class="info-item">
        <span>📍</span>
        <span class="info-label">Location:</span>
        <span>{loc_val}</span>
    </div>
    ''', unsafe_allow_html=True)

    # Pay info (salary/stipend)
    if pay:
        st.markdown(f'''
        <div class="info-item">
            <span>💰</span>
            <span class="info-label">{'Stipend' if source_name.lower()=='internshala' else 'Salary'}:</span>
            <span><strong>{pay}</strong></span>
        </div>
        ''', unsafe_allow_html=True)
    
    # Optional duration for Internshala
    if duration:
        st.markdown(f'''
        <div class="info-item">
            <span>⏳</span>
            <span class="info-label">Duration:</span>
            <span><strong>{duration}</strong></span>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply button
    st.markdown(f'''
    <div>
        <a href="{job_link}" target="_blank" style="text-decoration: none;">
            <div class="apply-button">Apply Now</div>
        </a>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bonus: bottom-right source tag (subtle)
    st.markdown(
        f"""
        <div style="display:flex; justify-content:flex-end; margin-top:6px;">
            <span style="font-size:11px; color:#9ca3af; background:rgba(255,255,255,0.04); border:1px solid #374151; padding:2px 8px; border-radius:999px;">{source_name}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

def course_recommender(course_list):
    """Display course recommendations - Catalog-style cards"""
    # Styles for course catalog cards
    st.markdown("""
        <style>
        @keyframes fadeInUp {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .course-card {
            background: linear-gradient(145deg, #0b1221, #151c30);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 18px 18px 16px 18px;
            margin: 10px 0 18px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.25);
            animation: fadeInUp .5s ease-out;
        }
        .course-header { display:flex; align-items:center; justify-content:space-between; gap:10px; }
        .course-title { color:#E6EAF3; font-size:18px; font-weight:800; margin:0; }
        .badge { display:inline-flex; align-items:center; gap:6px; padding:6px 10px; border-radius:999px; font-size:12px; font-weight:800; color:#fff; }
        .provider { color:#A6ADBB; font-size:13px; margin:8px 0 6px; font-weight:600; }
        .summary { color:#CBD5E1; font-size:13px; line-height:1.55; margin:0 0 10px; }
        .course-btn { display:inline-block; padding:10px 14px; border-radius:10px; color:#E0E7FF; font-weight:700; text-decoration:none; border:1px solid rgba(99,102,241,.35); background:linear-gradient(135deg, rgba(99,102,241,.15), rgba(139,92,246,.10)); }
        .course-btn:hover { filter:brightness(1.08); box-shadow:0 8px 18px rgba(99,102,241,.2); }
        </style>
    """, unsafe_allow_html=True)

    # Additional override styles for course cards (as requested)
    st.markdown("""
    <style>
    .course-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .course-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .course-header h3 {
        font-size: 1.1rem;
        margin-bottom: 6px;
        color: #e0e7ff;
    }
    .provider {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.6);
        margin-bottom: 10px;
    }
    .summary {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.7);
        margin-bottom: 15px;
    }
    .course-btn {
        display: inline-block;
        padding: 6px 12px;
        font-size: 0.85rem;
        color: #a78bfa;
        border: 1px solid rgba(167,139,250,0.3);
        border-radius: 8px;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .course-btn:hover {
        background: linear-gradient(90deg, #7c3aed, #2dd4bf);
        color: white;
        border-color: transparent;
    }
    .badge {
        background: linear-gradient(90deg, #7c3aed, #2dd4bf);
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header (centered)
    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <h2 style="color:#e0e7ff;">🎓 Recommended Courses</h2>
        <p style="color:rgba(255,255,255,0.7); font-size:0.95rem;">
            📘 Tailored learning paths to strengthen your profile and career growth
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not course_list:
        st.warning("No course recommendations available at the moment.")
        return []

    no_of_reco = st.selectbox(
        "Select how many recommendations you want to explore:",
        options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        index=5,
        key="courses_selectbox"
    )

    recommended_courses = random.sample(course_list, min(no_of_reco, len(course_list)))

    # Helper to render a single card
    def _render_course_card(title: str, link: str, idx: int):
        l = (link or '').lower()
        if 'udemy' in l:
            provider = 'Udemy'; badge_color = '#a855f7'
        elif 'coursera' in l:
            provider = 'Coursera'; badge_color = '#3b82f6'
        elif 'linkedin' in l:
            provider = 'LinkedIn Learning'; badge_color = '#0ea5e9'
        elif 'edx' in l:
            provider = 'edX'; badge_color = '#22c55e'
        else:
            provider = 'Online'; badge_color = '#22c55e'

        badges = []
        if idx == 0:
            badges.append('⭐ Top Match')
        if any(k in title.lower() for k in ['beginner', 'introduction', 'fundamentals']):
            badges.append('🧩 Beginner Friendly')
        if any(k in title.lower() for k in ['advanced', 'deep dive']):
            badges.append('⚡ Trending')

        # Simple summary fallback
        summary = ''
        # If we can infer a concise summary from title keywords
        if any(k in title.lower() for k in ['python','react','data','ml','ai','sql','django','flask','devops','cloud']):
            summary = f"Build practical skills in {title.split()[0]} with hands-on exercises."

        badge_spans = ''.join([f"<span class='badge' style='background:{badge_color};'>{b}</span>" for b in badges])

        # Avoid blank line ending HTML block: always include a summary paragraph (may be empty)
        summary_html = f"<p class='summary'>{summary}</p>" if summary else "<p class='summary'></p>"

        st.markdown(f"""
<div class="course-card">
  <div class="course-header">
    <h3 class="course-title">{title}</h3>
    <div>{badge_spans}</div>
  </div>
  <p class="provider">{provider}</p>
  {summary_html}
  <a href="{link}" target="_blank" class="course-btn">Explore Course →</a>
</div>
        """, unsafe_allow_html=True)

    # Layout: two columns if more than 4
    if len(recommended_courses) > 4:
        cols = st.columns(2)
        for i, (c_name, c_link) in enumerate(recommended_courses):
            with cols[i % 2]:
                _render_course_card(c_name, c_link, i)
    else:
        for i, (c_name, c_link) in enumerate(recommended_courses):
            _render_course_card(c_name, c_link, i)

    return [c_name for c_name, _ in recommended_courses]

def main():
    """Main application function"""
    # Initialize the application
    initialize_app()
    
    # Apply global styles from StyleManager
    StyleManager.apply_global_styles()
    StyleManager.apply_theme_styles("dark")
    
    # Modern Professional Dark Theme with Inter/Poppins
    st.markdown("""
    <style>
        /* ============ GLOBAL FONTS ============ */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
        /* ============ CSS COLOR VARIABLES ============ */
        :root {{
            /* Primary Colors */
            --primary: #7c3aed;
            --secondary: #2dd4bf;
            --primary-light: #8b5cf6;
            --primary-dark: #6d28d9;
            
            /* Text Colors */
            --text-main: #e2e8f0;
            --text-bright: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            
            /* Background Colors */
            --bg-dark: #0d1228;
            --bg-darker: #0a0f1f;
            --bg-card: rgba(15, 23, 42, 0.6);
            --bg-glass: rgba(15, 23, 42, 0.4);
            
            /* Accent & State Colors */
            --accent-purple: #7f5af0;
            --accent-teal: #2cb67d;
            --accent-blue: #38bdf8;
            --success: #46E1A1;
            
            /* Borders & Shadows */
            --border-color: rgba(255, 255, 255, 0.08);
            --border-light: rgba(255, 255, 255, 0.1);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
        }}
        
        /* ============ GLOBAL BODY & APP BACKGROUND ============ */
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
            background: radial-gradient(circle at top, var(--bg-dark), var(--bg-darker) 80%) !important;
            color: var(--text-main) !important;
            margin: 0;
            padding: 0;
        }}
        
        .stApp {{
            background: transparent !important;
        }}
        
        /* ============ TYPOGRAPHY ============ */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Poppins', sans-serif !important;
            font-weight: 700 !important;
            color: var(--text-main) !important;
            letter-spacing: -0.02em;
        }}
        
        h1 {{ font-size: 2.5rem !important; }}
        h2 {{ font-size: 2rem !important; }}
        h3 {{ font-size: 1.5rem !important; }}
        
        p, span, div, label {{
            font-family: 'Inter', sans-serif !important;
            color: var(--text-main) !important;
        }}
        
        /* ============ STREAMLIT COMPONENTS ============ */
        
        /* Buttons */
        .stButton>button {{
            background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.4rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            color: white !important;
            border: none !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3) !important;
        }}
        
        .stButton>button:hover {{
            transform: scale(1.05) !important;
            box-shadow: 0 0 20px rgba(124, 58, 237, 0.5) !important;
        }}
        
        /* Input Fields */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stSelectbox>div>div>div {{
            background: var(--bg-glass) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid var(--border-light) !important;
            border-radius: 8px !important;
            color: var(--text-main) !important;
            padding: 0.6rem 1rem !important;
            font-family: 'Inter', sans-serif !important;
        }}
        
        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {{
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
        }}
        
        /* Cards & Containers */
        .element-container, .stMarkdown {{
            margin: 0.5rem 0 !important;
        }}
        
        /* Glass effect panels */
        [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {{
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        
        /* ============ SIDEBAR DASHBOARD PANEL ============ */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0e132a 0%, #0a0d1b 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.05) !important;
            padding: 1.5rem 1rem !important;
        }}
        
        [data-testid="stSidebar"] * {{
            color: var(--text-main) !important;
        }}
        
        /* Sidebar headers with icons */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            color: var(--text-main) !important;
            margin-bottom: 1rem !important;
            padding-bottom: 0.5rem !important;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        /* Sidebar selectbox - glassy effect */
        [data-testid="stSidebar"] .stSelectbox {{
            margin-bottom: 1.5rem;
        }}
        
        [data-testid="stSidebar"] .stSelectbox label {{
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            margin-bottom: 0.5rem !important;
            color: var(--text-muted) !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox > div > div {{
            background: rgba(255, 255, 255, 0.04) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
            padding: 8px 12px !important;
            font-size: 0.95rem !important;
            transition: all 0.3s ease !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox > div > div:hover {{
            background: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(45, 212, 191, 0.4) !important;
            transform: translateY(-1px);
        }}
        
        [data-testid="stSidebar"] .stSelectbox > div > div > div {{
            color: var(--text-main) !important;
        }}
        
        /* Sidebar dividers */
        [data-testid="stSidebar"] hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            margin: 1.5rem 0;
        }}
        
        /* Sidebar links and text */
        [data-testid="stSidebar"] p {{
            font-size: 0.85rem;
            line-height: 1.6;
            color: var(--text-muted) !important;
        }}
        
        [data-testid="stSidebar"] a {{
            color: #94a3b8 !important;
            font-size: 0.95rem;
            text-decoration: none;
            transition: color 0.3s ease, transform 0.2s ease;
            display: inline-block;
        }}
        
        [data-testid="stSidebar"] a:hover {{
            color: #2dd4bf !important;
            transform: translateX(2px);
        }}
        
        /* Active menu item styling */
        [data-testid="stSidebar"] .active-item,
        [data-testid="stSidebar"] [data-selected="true"] {{
            background: rgba(99,102,241,0.15) !important;
            border-left: 3px solid #7c3aed !important;
            border-radius: 8px;
            padding-left: 0.75rem !important;
        }}
        
        /* Sidebar buttons */
        [data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.15), rgba(45, 212, 191, 0.15)) !important;
            border: 1px solid rgba(124, 58, 237, 0.3) !important;
            color: var(--text-main) !important;
            font-weight: 600 !important;
            padding: 0.75rem 1rem !important;
            border-radius: 8px !important;
            margin-bottom: 0.75rem;
        }}
        
        [data-testid="stSidebar"] .stButton > button:hover {{
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.25), rgba(45, 212, 191, 0.25)) !important;
            border-color: rgba(124, 58, 237, 0.5) !important;
            transform: translateY(-1px);
        }}
        
        /* Sidebar scrollbar */
        [data-testid="stSidebar"] ::-webkit-scrollbar {{
            width: 6px;
        }}
        
        [data-testid="stSidebar"] ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.03);
        }}
        
        [data-testid="stSidebar"] ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 3px;
        }}
        
        /* Selectbox */
        .stSelectbox>div>div>div>div>div>div {{
            color: var(--text-primary) !important;
            background-color: var(--bg-secondary) !important;
        }}
        
        /* File Uploader */
        [data-testid="stFileUploader"] {{
            background: var(--glass-bg) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
        }}
        
        [data-testid="stFileUploader"]>div>div>div>div>div>div {{
            color: var(--text-primary) !important;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: transparent;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            color: var(--text-secondary) !important;
            font-weight: 600;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(45, 212, 191, 0.2));
            color: var(--text-primary) !important;
            border-color: var(--accent-primary);
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background: var(--glass-bg) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 8px !important;
            color: var(--text-primary) !important;
            font-weight: 600 !important;
        }}
        
        /* Alerts */
        .stAlert {{
            background: var(--glass-bg) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 8px !important;
            color: var(--text-primary) !important;
        }}
        
        /* Spinner */
        .stSpinner>div {{
            border-top-color: var(--accent-primary) !important;
        }}
        
        /* DataFrames & Tables */
        .dataframe {{
            background: var(--glass-bg) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 8px !important;
            color: var(--text-primary) !important;
        }}
        
        /* Links */
        a {{
            color: #60a5fa !important;
            text-decoration: none;
        }}
        
        a:hover {{
            color: #93c5fd !important;
            text-decoration: underline;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--bg-primary);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, #7c3aed, #2dd4bf);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, #6d28d9, #14b8a6);
        }}
        
        /* Reduce excessive padding */
        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1100px;
            padding-left: 1.25rem !important;
            padding-right: 1.25rem !important;
        }}
        
        /* Consistent margins */
        .element-container {{
            margin-bottom: 0.75rem !important;
        }}
        
        /* ============ SECTION DIVIDERS ============ */
        /* Section title spacing */
        h2, h3 { margin-top: 36px !important; }
        .courses-title, .search-title, .section-title, .dashboard-title, .sugg-title, .role-title, .skills-header-text { margin-top: 36px !important; }
        .section-divider {{
            border: none;
            height: 1px;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent);
            margin: 60px 0;
        }}
        
        .section-divider-sm {{
            border: none;
            height: 1px;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.08), transparent);
            margin: 40px 0;
        }}
        
        .section-divider-lg {{
            border: none;
            height: 2px;
            background: linear-gradient(to right, transparent, rgba(124, 58, 237, 0.2), rgba(45, 212, 191, 0.2), transparent);
            margin: 80px 0;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Legacy dark theme overrides
    st.markdown("""
    <style>
        /* Ensure dark theme is applied to all elements */
        body {
            color: #F8FAFC !important;
            background-color: #0D1429 !important;
        }
        
        /* Ensure text color is consistent */
        .stApp, .stText, .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, 
        .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, 
        .stMarkdown li, .stMarkdown ol, .stMarkdown ul, .stMarkdown table,
        .stAlert, .stAlert p, .stAlert h1, .stAlert h2, .stAlert h3, .stAlert h4,
        .stAlert h5, .stAlert h6, .stAlert li, .stAlert ol, .stAlert ul, .stAlert table {
            color: #F8FAFC !important;
        }
        
        /* Style file uploader specifically */
        .stFileUploader > div > div > div > div > div > div {
            color: #F8FAFC !important;
        }
        
        /* Style select boxes */
        .stSelectbox > div > div > div > div > div > div {
            color: #F8FAFC !important;
        }
        
        /* Style input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            color: #F8FAFC !important;
            background-color: #1E293B !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main application
    if st.session_state.page == "analyzer":
        # Navigation Bar
        st.markdown("""
            <style>
            .nav-bar {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 15px 30px;
                border-radius: 12px;
                margin-bottom: 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }
            .nav-logo {
                font-size: 1.5rem;
                font-weight: 800;
                color: white;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .nav-links {
                display: flex;
            }
            </style>
        """, unsafe_allow_html=True)
        
        display_header()
        # Divider after Hero Section
        st.markdown("<hr style='margin: 40px 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);' />", unsafe_allow_html=True)
        
        # Sidebar with icons
        st.markdown("""
        <style>
        .sidebar-header {
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            color: #8b5cf6;
            margin: 20px 0 10px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 0 0 8px rgba(139,92,246,0.5);
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown("<div class='sidebar-header'>InternHunt Panel</div>", unsafe_allow_html=True)
        activities = ["User", "Admin"]
        choice = st.sidebar.selectbox("Select Mode", activities)
        
        st.sidebar.markdown("""
            <div style='text-align: center; font-size: 11px; color: #64748b; 
                        padding: 1rem 0; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 2rem;'>
                <div style='margin-bottom: 0.5rem; color: #94a3b8;'> 2024 InternHunt</div>
                <div>Developed by 
                <a href='https://www.linkedin.com/in/shubham-sharma-163a962a9' target='_blank'>Shubham</a>, 
                <a href='https://www.linkedin.com/in/abhinav-ghangas-5a3b8128a' target='_blank'>Abhinav</a>, 
                <a href='https://www.linkedin.com/in/pragya-9974b1298' target='_blank'>Pragya</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if choice == 'User':
            # Modern upload section styling
            st.markdown("""
                <style>
                /* ============ UPLOAD SECTION STYLING ============ */
                :root { 
                    --radius: 16px; 
                    --card-bg: rgba(255, 255, 255, 0.02); 
                    --muted: #94a3b8; 
                    --text: #e2e8f0; 
                    --text-bright: #f8fafc;
                }
                
                /* ============ UNIFIED ANIMATIONS ============ */
                /* Fade-in animation with cubic-bezier easing */
                .fade-in { 
                    animation: fadeIn 1s cubic-bezier(0.4, 0, 0.2, 1) both; 
                }
                
                @keyframes fadeIn { 
                    from {{ opacity: 0; transform: translateY(30px); }} 
                    to {{ opacity: 1; transform: translateY(0); }} 
                }}
                
                /* Modern upload card container with elevation */
                .upload-section,
                .card {{ 
                    background: rgba(255, 255, 255, 0.03);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    backdrop-filter: blur(12px);
                    border-radius: 20px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    padding: 24px;
                    transition: all 0.3s ease-in-out;
                    position: relative;
                }}
                
                .upload-card {{ 
                    padding: 1.75rem; 
                    margin: 1rem 0 1.5rem; 
                    position: relative;
                }}
                
                .upload-card::before {{
                    content: "";
                    position: absolute;
                    inset: -2px;
                    border-radius: 20px;
                    background: linear-gradient(135deg, rgba(124, 58, 237, 0.15), rgba(45, 212, 191, 0.15));
                    opacity: 0;
                    z-index: -1;
                    transition: opacity 0.3s ease;
                }}
                
                .upload-card:hover {{
                    border-color: rgba(124, 58, 237, 0.3);
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35), 0 0 30px rgba(124, 58, 237, 0.15);
                    transform: translateY(-4px);
                }}
                
                .upload-card:hover::before {{
                    opacity: 1;
                }}
                
                /* Upload card title with better contrast */
                .upload-card .title { 
                    font-size: 1.5rem; 
                    font-weight: 800; 
                    color: var(--text-bright); 
                    margin: 0 0 0.5rem; 
                    letter-spacing: -0.02em;
                    font-family: 'Poppins', sans-serif;
                }
                
                /* Subtitle with better readability */
                .upload-card .subtitle { 
                    color: var(--muted); 
                    font-size: 0.95rem; 
                    margin: 0 0 1rem; 
                    line-height: 1.6;
                }
                
                /* Soft divider */
                .soft-divider { 
                    height: 1px; 
                    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); 
                    margin: 1.25rem 0; 
                    border: none; 
                }
                
                /* File uploader styling */
                [data-testid="stFileUploader"] { 
                    background: transparent; 
                    text-align: center;
                }
                
                [data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] {{
                    background: rgba(255, 255, 255, 0.03);
                    border: 2px dashed rgba(124, 58, 237, 0.3);
                    border-radius: 12px;
                    padding: 2rem 1rem;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    min-height: 140px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                
                [data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"]:hover {{
                    background: rgba(124, 58, 237, 0.05);
                    border-color: rgba(124, 58, 237, 0.5);
                    box-shadow: 0 0 20px rgba(124, 58, 237, 0.1);
                }}
                
                /* Upload button */
                [data-testid="stFileUploader"] button {{ 
                    background: linear-gradient(135deg, #7c3aed, #2dd4bf) !important;
                    border: 0 !important;
                    color: white !important;
                    font-weight: 700 !important;
                    font-size: 0.95rem !important;
                    border-radius: 10px !important;
                    padding: 10px 20px !important;
                    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.3) !important;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                }}
                
                [data-testid="stFileUploader"] button:hover {{ 
                    filter: brightness(1.1) !important;
                    transform: translateY(-2px) !important;
                    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
                }}
                
                /* File pill badge */
                .file-pill { 
                    display: flex; 
                    align-items: center; 
                    gap: 0.75rem; 
                    padding: 0.75rem 1rem; 
                    border-radius: 12px; 
                    background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(45, 212, 191, 0.15)); 
                    border: 1px solid rgba(124, 58, 237, 0.35); 
                    color: var(--text-bright); 
                    font-weight: 700; 
                    font-size: 0.95rem;
                }
                
                .file-pill .icon { 
                    font-size: 1.25rem; 
                }
                
                /* Success badge */
                .badge-success { 
                    display: inline-flex; 
                    align-items: center; 
                    gap: 0.4rem; 
                    font-size: 0.8rem; 
                    font-weight: 700; 
                    color: #46E1A1; 
                    background: rgba(16, 185, 129, 0.12); 
                    border: 1px solid rgba(16, 185, 129, 0.35); 
                    padding: 0.35rem 0.7rem; 
                    border-radius: 999px; 
                }
                
                /* Meta text */
                .meta { 
                    color: #94a3b8; 
                    font-size: 0.8rem; 
                    margin-top: 0.5rem; 
                }
                
                /* Chip badge */
                .chip { 
                    display: inline-flex; 
                    align-items: center; 
                    gap: 0.4rem; 
                    padding: 0.4rem 0.8rem; 
                    border-radius: 999px; 
                    font-size: 0.8rem; 
                    font-weight: 600; 
                    border: 1px solid rgba(255, 255, 255, 0.1); 
                    color: #cbd5e1; 
                    background: rgba(255, 255, 255, 0.05); 
                }
                
                /* Links */
                a.inline { 
                    color: #60a5fa; 
                    text-decoration: none; 
                    transition: all 0.2s ease;
                }
                
                a.inline:hover { 
                    color: #93c5fd;
                    text-decoration: underline; 
                }
                </style>
            """, unsafe_allow_html=True)

            # Divider before upload section
            st.markdown('<hr class="section-divider-lg">', unsafe_allow_html=True)
            
            up_left, up_right = st.columns([3, 1])
            with up_left:
                st.markdown('<div id="upload-section" class="card upload-card fade-in">\
                    <div class="title">Upload Resume</div>\
                    <div class="subtitle">PDF only. Keep it under 10MB.</div>', unsafe_allow_html=True)
                pdf_file = st.file_uploader("Upload Resume", type=["pdf"], label_visibility="collapsed", key="resume_pdf")
                st.markdown('<hr class="soft-divider"/>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with up_right:
                # Show file details card when available
                if 'resume_pdf' in st.session_state and st.session_state['resume_pdf'] is not None:
                    _f = st.session_state['resume_pdf']
                    _size_kb = getattr(_f, 'size', 0) // 1024
                    _ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                    st.markdown(f"""
                        <div class='card fade-in' style='margin-top:.6rem;'>
                            <div class='file-pill'><span class='icon'>📄</span><span>{_f.name}</span></div>
                            <div style='margin-top:.45rem; display:flex; align-items:center; justify-content:space-between;'>
                                <span class='badge-success'>✓ Uploaded Successfully</span>
                                <span class='chip'>Secure</span>
                            </div>
                            <div class='meta'>Size: {_size_kb} KB • Uploaded: {_ts}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class='card fade-in' style='margin-top:.6rem;'>
                            <div class='meta'>No file selected.</div>
                        </div>
                    """, unsafe_allow_html=True)

            # Initialize resume_data
            resume_data = None
            
            if pdf_file is not None:
                st.session_state['resume_upload_attempted'] = True
                with st.spinner("Uploading and analyzing your resume..."):
                    time.sleep(1)
                
                # Save uploaded file
                save_path = os.path.join(Config.UPLOAD_DIR, pdf_file.name)
                os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
                
                with open(save_path, "wb") as f:
                    f.write(pdf_file.getbuffer())
                
                # Track current resume to reset chat state if needed
                try:
                    current_resume_id = f"{save_path}:{os.path.getsize(save_path)}"
                except Exception:
                    current_resume_id = save_path
                if st.session_state.get('resume_id') != current_resume_id:
                    # New file uploaded: parse and cache
                    with st.spinner("🔍 Analyzing your resume..."):
                        parser = get_resume_parser()
                        resume_data = parser.parse_resume(pdf_file)
                        
                        # Predict category using ML model
                        resume_text = resume_data.get('raw_text', '')  # Use raw_text from parser
                        if resume_text:
                            try:
                                predicted_cat, top_3 = predict_resume_category(resume_text)
                                if predicted_cat:
                                    resume_data['predicted_category'] = predicted_cat
                                    resume_data['top_3_categories'] = top_3
                                    # Success - no need to show message, it's displayed in the card below
                                # else:
                                #     st.warning("⚠️ ML Model could not predict category")
                            except Exception as e:
                                pass  # Silent fail - prediction is optional
                                # st.error(f"❌ ML prediction failed: {e}")
                        
                        st.session_state['resume_id'] = current_resume_id
                        st.session_state['resume_path'] = save_path
                        st.session_state['resume_data'] = resume_data
                        st.session_state['chat_messages'] = []
                else:
                    # Same file selected; reuse cached parsed data
                    resume_data = st.session_state.get('resume_data')
            else:
                # Use cached parsed resume
                resume_data = st.session_state.get('resume_data')
                # If missing, try to re-parse from saved path to survive reruns/errors
                resume_path = st.session_state.get('resume_path')
                if not resume_data and resume_path and os.path.exists(resume_path):
                    try:
                        parser = get_resume_parser()
                        with open(resume_path, "rb") as f:
                            resume_data = parser.parse_resume(f)
                        st.session_state['resume_data'] = resume_data
                    except Exception:
                        pass
            
            if resume_data:
                # Divider before results section
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
                
                # Display candidate info - Modern Card Design
                st.markdown(f"""
                <style>
                @keyframes shimmer {{
                    0% {{ left: -100%; }}
                    100% {{ left: 100%; }}
                }}
                
                @keyframes cardSlideIn {{
                    0% {{ 
                        opacity: 0;
                        transform: translateY(10px);
                    }}
                    100% {{ 
                        opacity: 1;
                        transform: translateY(0px);
                    }}
                }}
                </style>
                """, unsafe_allow_html=True)
                
                # Allow user to pick a target role to improve role alignment
                role = st.sidebar.selectbox(
                    "Target role (for ATS alignment)",
                    ["Auto-detect", "Software Engineer", "Data Analyst", "Web Developer", "Machine Learning Engineer"],
                    index=0,
                    key="target_role_select"
                )
                _resume_for_score = dict(resume_data)
                if role != "Auto-detect":
                    _resume_for_score["target_role"] = role
                breakdown = AnalyticsUtils.calculate_resume_score_breakdown(_resume_for_score)
                score = breakdown.get("total", 0)
                components = breakdown.get("components", {})
                sections_presence = components.get('sections_presence') or {}
                suggestions = breakdown.get("suggestions", [])
                scores_summary = breakdown.get("scores", {})

                # Profile Overview Card (sleek, minimal)
                subtitle = "Candidate Profile"
                email = resume_data.get('email') or 'N/A'
                phone = resume_data.get('mobile_number') or 'N/A'
                linkedin = resume_data.get('linkedin')
                github = resume_data.get('github')
                
                # Build contact cards dynamically
                contact_cards = []
                contact_cards.append(f'<div class="ov-card-mini">📧 {email}</div>')
                contact_cards.append(f'<div class="ov-card-mini">📞 {phone}</div>')
                if linkedin or github:
                    raw_link = linkedin if linkedin else github
                    def _pick_link(v):
                        if isinstance(v, (list, tuple, set)):
                            for x in v:
                                if isinstance(x, str) and x.strip():
                                    return x.strip()
                            return None
                        if isinstance(v, dict):
                            for k in ("url", "href", "link", "profile", "username"):
                                val = v.get(k)
                                if isinstance(val, str) and val.strip():
                                    return val.strip()
                            return None
                        if isinstance(v, str):
                            s = v.strip()
                            return s or None
                        return None
                    link_text = _pick_link(raw_link)
                    if link_text:
                        lt = link_text
                        lower = lt.lower()
                        link_href = lt if lower.startswith(("http://", "https://")) else ("https://" + lt.lstrip("/"))
                        link_disp = lt.replace("https://", "").replace("http://", "")
                        contact_cards.append(f'<div class="ov-card-mini">🔗 <a class="inline" href="{link_href}" target="_blank">{link_disp}</a></div>')

                st.markdown(f"""
                <style>
                .ov-card {{
                    background: linear-gradient(145deg, #0b1221, #151c30);
                    border: 1px solid rgba(255,255,255,0.06);
                    border-radius: 20px;
                    padding: 1.2rem 1.4rem;
                    margin: 0.8rem 0 1.4rem;
                    box-shadow: 0 12px 32px rgba(0,0,0,0.35);
                }}
                .ov-header {{ display:flex; align-items:center; gap:14px; margin-bottom:.6rem; }}
                .ov-avatar {{ width:54px;height:54px;border-radius:50%;background:linear-gradient(135deg,#4f46e5,#06b6d4);display:flex;align-items:center;justify-content:center;color:white;font-weight:900; }}
                .ov-name {{ color:#fff; font-weight:900; font-size:24px; letter-spacing:-0.3px; }}
                .ov-sub {{ color:#A6ADBB; font-size:14px; margin-top:2px; }}
                .ov-cards {{ display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; }}
                .ov-card-mini {{ display:flex; align-items:center; gap:8px; border:1px solid rgba(255,255,255,.08); background: linear-gradient(145deg, rgba(255,255,255,.06), rgba(255,255,255,.03)); padding:10px 12px; border-radius:12px; color:#E6EAF3; }}
                .separator-soft {{ height:1px; background: linear-gradient(90deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02), rgba(255,255,255,0.06)); margin-top:.9rem; }}
                .ov-card a.inline:hover {{ filter: brightness(1.08); }}
                @media (max-width: 900px) {{ .ov-cards {{ grid-template-columns: 1fr; }} }}
                </style>
                <div class="ov-card fade-in">
                  <div class="ov-header">
                    <div class="ov-avatar">{(resume_data.get('name','?') or '?')[:1].upper()}</div>
                    <div>
                      <div class="ov-name">{resume_data.get('name') or 'Candidate'}</div>
                      <div class="ov-sub">{subtitle}</div>
                    </div>
                  </div>
                  <div class="ov-cards">
                    {''.join(contact_cards)}
                  </div>
                  <div class="separator-soft"></div>
                </div>
                """, unsafe_allow_html=True)
                
                # Skills Extracted (moved up before AI-Detected Profile)
                st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 40px 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);' />", unsafe_allow_html=True)
                skills = resume_data.get('skills', [])
                if skills:
                    categorized_skills = categorize_skills(skills)
                    display_skills(categorized_skills)
                    st.markdown("<hr style='margin: 40px 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);' />", unsafe_allow_html=True)
                
                # ML Category Prediction Badge
                predicted_cat = resume_data.get('predicted_category')
                top_3 = resume_data.get('top_3_categories', [])
                
                if predicted_cat and top_3:
                    confidence = top_3[0]['probability'] * 100 if top_3 else 0
                    
                    # Build top 3 predictions HTML
                    top_3_html = ""
                    for i, pred in enumerate(top_3[:3]):
                        prob = pred['probability'] * 100
                        category = pred['category']
                        icon = "🎯" if i == 0 else "🔹" if i == 1 else "🔸"
                        top_3_html += f'<div class="pred-item">{icon} <span class="pred-cat">{category}</span> <span class="pred-prob">{prob:.1f}%</span></div>'
                    
                    st.markdown(f"""
                    <style>
                    .ml-prediction-card {{
                        background: linear-gradient(145deg, #0b1221, #151c30);
                        border: 2px solid rgba(99, 102, 241, 0.3);
                        border-radius: 20px;
                        padding: 20px 24px;
                        margin: 12px 0 20px;
                        box-shadow: 0 12px 32px rgba(99, 102, 241, 0.15), 0 0 40px rgba(99, 102, 241, 0.08);
                        position: relative;
                        overflow: hidden;
                    }}
                    .ml-prediction-card::before {{
                        content: '';
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        height: 3px;
                        background: linear-gradient(90deg, #6366F1, #8B5CF6, #06B6D4);
                    }}
                    .ml-header {{
                        display: flex;
                        align-items: center;
                        gap: 12px;
                        margin-bottom: 16px;
                    }}
                    .ml-icon {{
                        width: 42px;
                        height: 42px;
                        background: linear-gradient(135deg, #6366F1, #8B5CF6);
                        border-radius: 12px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 20px;
                        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.3);
                    }}
                    .ml-title {{
                        font-size: 18px;
                        font-weight: 800;
                        color: #E6EAF3;
                        margin: 0;
                    }}
                    .ml-badge {{
                        display: inline-flex;
                        align-items: center;
                        gap: 8px;
                        padding: 10px 16px;
                        border-radius: 12px;
                        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.15));
                        border: 1px solid rgba(99, 102, 241, 0.4);
                        margin-bottom: 14px;
                    }}
                    .ml-badge-label {{
                        font-size: 14px;
                        color: #A6ADBB;
                        font-weight: 600;
                    }}
                    .ml-badge-value {{
                        font-size: 18px;
                        color: #E6EAF3;
                        font-weight: 800;
                    }}
                    .ml-badge-conf {{
                        font-size: 13px;
                        color: #22C55E;
                        font-weight: 700;
                        background: rgba(34, 197, 94, 0.15);
                        padding: 4px 10px;
                        border-radius: 8px;
                        border: 1px solid rgba(34, 197, 94, 0.3);
                    }}
                    .top-predictions {{
                        display: flex;
                        flex-direction: column;
                        gap: 8px;
                        padding: 14px;
                        background: rgba(255, 255, 255, 0.02);
                        border-radius: 12px;
                        border: 1px solid rgba(255, 255, 255, 0.06);
                    }}
                    .pred-item {{
                        display: flex;
                        align-items: center;
                        gap: 10px;
                        font-size: 14px;
                        color: #D9E2F1;
                    }}
                    .pred-cat {{
                        flex: 1;
                        font-weight: 600;
                    }}
                    .pred-prob {{
                        font-weight: 700;
                        color: #8B5CF6;
                    }}
                    </style>
                    
                    <div class="ml-prediction-card fade-in">
                        <div class="ml-header">
                            <div class="ml-icon">🤖</div>
                            <div class="ml-title">AI-Detected Profile</div>
                        </div>
                        <div class="ml-badge">
                            <span class="ml-badge-label">Category:</span>
                            <span class="ml-badge-value">{predicted_cat}</span>
                            <span class="ml-badge-conf">{confidence:.1f}% match</span>
                        </div>
                        <div class="top-predictions">
                            {top_3_html}
                    </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Divider after AI-Detected Profile
                st.markdown("<hr style='margin: 40px 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);' />", unsafe_allow_html=True)

                # Premium ATS Score Dashboard
                st.markdown("""
                <style>
                .ats-dashboard {
                    background: linear-gradient(135deg, #1A1F3A 0%, #242F5C 50%, #1A1F3A 100%);
                    border: 1.5px solid rgba(99, 102, 241, 0.3);
                    border-radius: 20px;
                    padding: 40px;
                    margin: 40px 0;
                    box-shadow: 0 15px 50px rgba(99, 102, 241, 0.12), 0 0 30px rgba(99, 102, 241, 0.05);
                    position: relative;
                    overflow: hidden;
                }
                
                .ats-dashboard::before {
                    content: '';
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: conic-gradient(from 0deg, transparent, rgba(99, 102, 241, 0.03), transparent);
                    animation: rotate 20s linear infinite;
                }
                
                @keyframes rotate {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                
                .dashboard-header {
                    display: flex;
                    align-items: center;
                    gap: 16px;
                    margin-bottom: 32px;
                    position: relative;
                    z-index: 2;
                }
                
                .dashboard-title {
                    font-size: 24px;
                    font-weight: 800;
                    color: #E0E7FF;
                    margin: 0;
                }
                
                .dashboard-icon {
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, #6366F1, #8B5CF6);
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 20px;
                    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
                }
                
                .score-overview {
                    display: grid;
                    grid-template-columns: 1fr 2fr;
                    gap: 40px;
                    margin-bottom: 40px;
                    position: relative;
                    z-index: 2;
                }
                
                .score-gauge-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                }
                
                .score-gauge {
                    width: 160px;
                    height: 160px;
                    position: relative;
                    margin-bottom: 20px;
                }
                
                .score-gauge svg {
                    transform: rotate(-90deg);
                    width: 100%;
                    height: 100%;
                }
                
                .score-gauge-bg {
                    fill: none;
                    stroke: rgba(75, 85, 99, 0.2);
                    stroke-width: 10;
                }
                
                .score-gauge-progress {
                    fill: none;
                    stroke-width: 10;
                    stroke-linecap: round;
                    filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.5));
                    transition: stroke-dashoffset 1.5s ease-out;
                }
                
                .score-gauge-inner {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 130px;
                    height: 130px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #0F1629, #1A1F3A);
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    border: 2px solid rgba(99, 102, 241, 0.2);
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                }
                
                .score-number {
                    font-size: 32px;
                    font-weight: 900;
                    color: #10B981;
                    line-height: 1;
                }
                
                .score-label {
                    font-size: 12px;
                    color: #9CA3AF;
                    margin-top: 4px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                
                .score-grade {
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    padding: 8px 16px;
                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 20px;
                    color: #34D399;
                    font-size: 14px;
                    font-weight: 700;
                }
                
                .sections-overview {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                    gap: 20px;
                    margin-bottom: 40px;
                    position: relative;
                    z-index: 2;
                }
                
                .section-card-premium {
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(139, 92, 246, 0.03));
                    border: 1px solid rgba(99, 102, 241, 0.2);
                    border-radius: 16px;
                    padding: 24px;
                    text-align: center;
                    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                    position: relative;
                    overflow: hidden;
                    backdrop-filter: blur(10px);
                }
                
                .section-card-premium::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 3px;
                    background: linear-gradient(90deg, transparent, var(--status-color), transparent);
                    transition: all 0.3s ease;
                }
                
                .section-card-premium:hover {
                    transform: translateY(-8px);
                    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
                    border-color: rgba(167, 139, 250, 0.4);
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(139, 92, 246, 0.06));
                }
                
                .section-card-premium:hover::before {
                    height: 4px;
                    box-shadow: 0 0 20px var(--status-color);
                }
                
                .section-icon-modern {
                    width: 48px;
                    height: 48px;
                    margin: 0 auto 16px;
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    position: relative;
                    transition: all 0.3s ease;
                }
                
                .section-name-modern {
                    color: #E0E7FF;
                    font-size: 14px;
                    font-weight: 700;
                    margin-bottom: 12px;
                }
                
                .status-indicator {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 6px;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 600;
                    position: relative;
                }
                
                .status-present-premium {
                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.05));
                    border: 1px solid rgba(16, 185, 129, 0.4);
                    color: #34D399;
                }
                
                .status-missing-premium {
                    background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.05));
                    border: 1px solid rgba(245, 158, 11, 0.4);
                    color: #FBBF24;
                }
                
                .insights-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 24px;
                    position: relative;
                    z-index: 2;
                }
                
                .insights-panel {
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.02));
                    border: 1px solid rgba(99, 102, 241, 0.15);
                    border-radius: 16px;
                    padding: 24px;
                    backdrop-filter: blur(10px);
                    transition: all 0.3s ease;
                }
                
                .insights-panel:hover {
                    border-color: rgba(167, 139, 250, 0.3);
                    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.1);
                }
                
                .panel-header {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    margin-bottom: 16px;
                }
                
                .panel-icon {
                    width: 32px;
                    height: 32px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 16px;
                }
                
                .panel-title {
                    color: #E0E7FF;
                    font-size: 16px;
                    font-weight: 700;
                    margin: 0;
                }
                
                .insight-item {
                    display: flex;
                    align-items: flex-start;
                    gap: 12px;
                    padding: 12px 0;
                    border-bottom: 1px solid rgba(99, 102, 241, 0.1);
                }
                
                .insight-item:last-child {
                    border-bottom: none;
                    padding-bottom: 0;
                }
                
                .insight-item:first-child {
                    padding-top: 0;
                }
                
                .insight-icon {
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 10px;
                    flex-shrink: 0;
                    margin-top: 2px;
                }
                
                .insight-text {
                    color: #CBD5E1;
                    font-size: 14px;
                    line-height: 1.5;
                    font-weight: 500;
                }
                
                .strength-icon {
                    background: linear-gradient(135deg, #10B981, #059669);
                    color: white;
                }
                
                .improvement-icon {
                    background: linear-gradient(135deg, #F59E0B, #D97706);
                    color: white;
                }
                
                @media (max-width: 768px) {
                    .score-overview {
                        grid-template-columns: 1fr;
                        text-align: center;
                    }
                    
                    .sections-overview {
                        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                    }
                    
                    .insights-grid {
                        grid-template-columns: 1fr;
                    }
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Get the feedback data
                feedback = breakdown.get('feedback')
                strong_areas = breakdown.get('strong_areas', [])
                weak_areas = breakdown.get('weak_areas', [])
                
                # Determine score color and grade
                if score >= 85:
                    grade = "Excellent"
                    score_color = "#10B981"
                    grade_icon = "🎯"
                elif score >= 70:
                    grade = "Good"
                    score_color = "#34D399"
                    grade_icon = "✅"
                elif score >= 55:
                    grade = "Fair"
                    score_color = "#F59E0B"
                    grade_icon = "⚡"
                else:
                    grade = "Needs Work"
                    score_color = "#EF4444"
                    grade_icon = "🔧"
                
                # Calculate SVG circle parameters
                radius = 70  # SVG circle radius
                circumference = 2 * 3.14159 * radius  # ~439.8
                # For stroke-dashoffset: 
                # - Full circumference = 0% filled (circle hidden)
                # - 0 = 100% filled (full circle)
                # So for 75%, we want 25% remaining = circumference * 0.25
                progress_offset = circumference * (100 - score) / 100
                
                # Top margin before ATS dashboard
                st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)
                
                # Build dashboard using component approach
                dashboard_parts = [
                    '<div class="ats-dashboard">',
                    '<div class="dashboard-header">',
                    '<div class="dashboard-icon">🎯</div>',
                    '<h2 class="dashboard-title">ATS Performance Dashboard</h2>',
                    '</div>',
                    '<div class="score-overview">',
                    '<div class="score-gauge-container">',
                    f'<div class="score-gauge">',
                    '<svg width="160" height="160" viewBox="0 0 160 160">',
                    # Background circle
                    '<circle class="score-gauge-bg" cx="80" cy="80" r="70" />',
                    # Progress circle with inline styles for dasharray and dashoffset
                    f'<circle class="score-gauge-progress" cx="80" cy="80" r="70" style="stroke: {score_color}; stroke-dasharray: {circumference}; stroke-dashoffset: {progress_offset};" />',
                    '</svg>',
                    '<div class="score-gauge-inner">',
                    f'<div class="score-number" style="color: {score_color};">{score}</div>',
                    '<div class="score-label">/ 100</div>',
                    '</div>',
                    '</div>',
                    '<div class="score-grade">',
                    f'<span>{grade_icon}</span>',
                    f'<span>{grade}</span>',
                    '</div>',
                    '</div>',
                    '<div style="display: flex; flex-direction: column; justify-content: center; gap: 16px;">',
                ]
                
                # Add score breakdown metrics instead of feedback text
                if scores_summary:
                    dashboard_parts.extend([
                        '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">'
                    ])
                    
                    max_map = {
                        'content_quality': 50,
                        'formatting': 15,
                        'keyword_relevance': 20,
                        'experience_impact': 10,
                        'readability': 5,
                    }
                    
                    for k, v in scores_summary.items():
                        label = k.replace('_', ' ').title()
                        denom = max_map.get(k, 100)
                        val = round(float(v), 1) if isinstance(v, (int, float)) else v
                        percentage = int((val / denom) * 100) if denom > 0 else 0
                        
                        dashboard_parts.extend([
                            '<div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.05)); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 16px;">',
                            f'<div style="color: #E0E7FF; font-size: 14px; font-weight: 700; margin-bottom: 8px;">{label}</div>',
                            f'<div style="color: #818CF8; font-size: 18px; font-weight: 800;">{val}/{denom}</div>',
                            f'<div style="background: rgba(99, 102, 241, 0.1); height: 4px; border-radius: 2px; margin-top: 8px; overflow: hidden;">',
                            f'<div style="background: linear-gradient(90deg, #6366F1, #8B5CF6); height: 100%; width: {percentage}%; border-radius: 2px; transition: width 0.3s ease;"></div>',
                            '</div>',
                            '</div>'
                        ])
                    
                    dashboard_parts.append('</div>')
                
                dashboard_parts.extend([
                    '</div>',
                    '</div>',
                    '<div class="sections-overview">'
                ])
                
                # Add the enhanced section cards
                items = [
                    ('Experience', 'experience', '💼'),
                    ('Education', 'education', '🎓'),
                    ('Skills', 'skills', '🛠️'),
                    ('Summary', 'summary', '📝'),
                    ('Projects', 'projects', '🚀'),
                ]
                
                for label, key_, icon in items:
                    ok = bool(sections_presence.get(key_))
                    status_class = 'status-present-premium' if ok else 'status-missing-premium'
                    status_color = '#10B981' if ok else '#F59E0B'
                    status_text = 'Present' if ok else 'Missing'
                    status_icon = '✓' if ok else '⚠'
                    
                    dashboard_parts.extend([
                        f'<div class="section-card-premium" style="--status-color: {status_color};">',
                        f'<div class="section-icon-modern" style="background: linear-gradient(135deg, {status_color}20, {status_color}10);">{icon}</div>',
                        f'<div class="section-name-modern">{label}</div>',
                        f'<div class="status-indicator {status_class}">',
                        f'<span>{status_icon}</span>',
                        f'<span>{status_text}</span>',
                        '</div>',
                        '</div>'
                    ])
                
                dashboard_parts.extend([
                    '</div>',
                    '<div class="insights-grid">'
                ])
                
                # Strengths panel
                if strong_areas:
                    dashboard_parts.extend([
                        '<div class="insights-panel">',
                        '<div class="panel-header">',
                        '<div class="panel-icon" style="background: linear-gradient(135deg, #10B981, #059669); color: white;">✓</div>',
                        '<h3 class="panel-title">Strengths</h3>',
                        '</div>'
                    ])
                    
                    for strength in strong_areas[:4]:  # Limit to top 4
                        dashboard_parts.extend([
                            '<div class="insight-item">',
                            '<div class="insight-icon strength-icon">✓</div>',
                            f'<div class="insight-text">{strength}</div>',
                            '</div>'
                        ])
                    
                    dashboard_parts.append('</div>')
                
                # Areas for improvement panel
                if weak_areas:
                    dashboard_parts.extend([
                        '<div class="insights-panel">',
                        '<div class="panel-header">',
                        '<div class="panel-icon" style="background: linear-gradient(135deg, #F59E0B, #D97706); color: white;">⚡</div>',
                        '<h3 class="panel-title">Areas for Improvement</h3>',
                        '</div>'
                    ])
                    
                    for area in weak_areas[:4]:  # Limit to top 4
                        dashboard_parts.extend([
                            '<div class="insight-item">',
                            '<div class="insight-icon improvement-icon">!</div>',
                            f'<div class="insight-text">{area}</div>',
                            '</div>'
                        ])
                    
                    dashboard_parts.append('</div>')
                
                dashboard_parts.extend(['</div>', '</div>'])
                
                st.markdown(''.join(dashboard_parts), unsafe_allow_html=True)

                # Divider after ATS Performance Dashboard
                st.markdown("<hr style='margin: 40px 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);' />", unsafe_allow_html=True)

                # Resume Analysis Section (moved here after ATS)
                st.markdown("""
                <style>
                .analysis-section { background: linear-gradient(145deg, #0b1221, #151c30); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:22px; margin: 18px 0 14px; box-shadow:0 10px 30px rgba(0,0,0,.35); }
                .section-header { display:flex; flex-direction:column; align-items:flex-start; gap:6px; margin-bottom: 12px; }
                .section-title { font-size:22px; font-weight:800; color:#E6EAF3; margin:0; }
                .section-sub { font-size:14px; color:#9AA4B2; margin:0; }
                .summary-row { display:flex; gap:12px; flex-wrap:wrap; align-items:center; }
                .pill { display:inline-flex; align-items:center; gap:.45rem; padding:.5rem .8rem; border-radius:999px; font-size:13px; font-weight:700; color:#E6EAF3; border:1px solid rgba(255,255,255,.08); background: linear-gradient(145deg, rgba(99,102,241,.18), rgba(139,92,246,.12)); }
                .pill.alt { background: linear-gradient(145deg, rgba(34,197,94,.18), rgba(20,184,166,.12)); border-color: rgba(20,184,166,.35); }
                .mini-progress { width: 160px; height: 6px; background: rgba(255,255,255,.06); border-radius: 999px; overflow: hidden; border:1px solid rgba(255,255,255,.08); }
                .mini-bar { height: 100%; background: linear-gradient(90deg, #22C55E, #06B6D4); width: 0; border-radius: 999px; transition: width .6s ease; }
                </style>
                """, unsafe_allow_html=True)

                # Calculate stats for the summary
                skills_count = len(resume_data.get('skills') or [])
                sections_presence = components.get('sections_presence') or {}
                present_count = sum(1 for k in ['experience','education','skills','summary','projects'] if sections_presence.get(k))
                percent = int((present_count/5)*100)

                st.markdown(
                    f"""
                    <div class='analysis-section fade-in'>
                        <div class='section-header'>
                            <h2 class='section-title'>Resume Analysis</h2>
                            <div class='section-sub'>Overview of detected skills and resume completeness.</div>
                        </div>
                        <div class='summary-row'>
                            <span class='pill'>🧰 Skills <b>{skills_count}</b></span>
                            <span class='pill alt'>📚 Sections <b>{present_count}/5</b></span>
                            <div class='mini-progress'><div class='mini-bar' style='width:{percent}%;'></div></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Divider after Resume Analysis
                st.markdown("<hr style='margin: 40px 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);' />", unsafe_allow_html=True)

                if suggestions:
                    # Styles for nicer suggestions list and expanders
                    st.markdown("""
                    <style>
                    .sugg-wrap { margin-top: 16px; }
                    .sugg-title { color:#FFFFFF; margin-bottom:12px; font-weight:800; }
                    .sugg-list { display:flex; flex-direction:column; gap:8px; }
                    .sugg-item { display:flex; align-items:flex-start; gap:10px; padding:10px 12px; border-radius:12px; border:1px solid rgba(99,102,241,.25); background:linear-gradient(135deg, rgba(99,102,241,.10), rgba(37,99,235,.08)); }
                    .sugg-num { width:26px; height:26px; border-radius:999px; display:inline-flex; align-items:center; justify-content:center; font-weight:800; color:#E0E7FF; background:rgba(99,102,241,.35); border:1px solid rgba(99,102,241,.45); }
                    .sugg-text { color:#E0E7FF; font-size:14px; font-weight:600; }
                    [data-testid=\"stExpander\"] { border:1px solid rgba(99,102,241,.25); border-radius:12px; background:linear-gradient(135deg,#0F1534,#121A3F); }
                    [data-testid=\"stExpander\"] > summary { color:#E0E7FF; font-weight:700; }
                    [data-testid=\"stCodeBlock\"] pre { background:#0B1220 !important; border:1px solid rgba(99,102,241,.25); border-radius:10px; }
                    /* Template cards */
                    .tpl-card { border:1px solid rgba(99,102,241,.35); border-radius:12px; background:linear-gradient(135deg,#0B1220,#11183A); padding:14px; }
                    .tpl-head { display:flex; align-items:center; gap:8px; color:#E0E7FF; font-weight:800; margin-bottom:6px; }
                    .tpl-tags { display:flex; gap:6px; flex-wrap:wrap; margin-bottom:8px; }
                    .tpl-tag { background:rgba(99,102,241,.15); border:1px solid rgba(99,102,241,.35); color:#E0E7FF; padding:2px 8px; border-radius:999px; font-size:12px; font-weight:600; }
                    .tpl-pre { margin:0; white-space:pre-wrap; color:#E5E7EB; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, \'Liberation Mono\', \'Courier New\', monospace; font-size:13px; line-height:1.55; }
                    .tpl-tips { margin-top:8px; color:#A5B4FC; font-size:12px; }
                    </style>
                    """, unsafe_allow_html=True)

                    # Header
                    st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)
                    st.markdown('<div class="sugg-wrap"><h3 class="sugg-title">💡 Top Suggestions</h3>', unsafe_allow_html=True)

                    # Suggestions list
                    rows = [
                        f"<div class='sugg-item'><span class='sugg-num'>{idx}</span><span class='sugg-text'>{s}</span></div>"
                        for idx, s in enumerate(suggestions, start=1)
                    ]
                    st.markdown(f"<div class='sugg-list'>{''.join(rows)}</div>", unsafe_allow_html=True)

                    # Templates for missing sections
                    st.markdown("""
                    <style>
                    .tpl-card {
                        background-color: #0f1720;
                        border-radius: 12px;
                        padding: 16px;
                        margin-bottom: 16px;
                        border: 1px solid rgba(255,255,255,0.04);
                    }
                    .tpl-head {
                        font-size: 18px;
                        font-weight: 600;
                        color: #e6eef8;
                        margin-bottom: 8px;
                    }
                    .tpl-tags { margin-bottom: 10px; }
                    .tpl-tag {
                        display: inline-block;
                        background: linear-gradient(90deg,#5b8cff,#8b5cf6);
                        color: #fff;
                        padding: 5px 10px;
                        border-radius: 999px;
                        font-size: 12px;
                        margin-right: 6px;
                    }
                    .tpl-pre {
                        background-color: #0b0d11;
                        color: #dbeafe;
                        padding: 12px;
                        border-radius: 8px;
                        line-height: 1.6;
                        white-space: pre-line; /* preserves newlines while allowing wrapping */
                        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", "Courier New", monospace;
                        font-size: 13px;
                        border-left: 3px solid rgba(99,102,241,0.85);
                        margin-top: 8px;
                    }
                    .tpl-tips {
                        margin-top: 10px;
                        color: #9aa4b2;
                        font-size: 13px;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                    # --- Prepare variables ---
                    sp = components.get('sections_presence') or {}
                    top_skills = (resume_data.get('skills') or [])[:3]
                    role_for_tpl = role if role != 'Auto-detect' else (components.get('kw_role_alignment_role') or 'Software Engineer')
                    role_skills = ', '.join(top_skills) if top_skills else 'relevant tools/skills'

                    # --- Work Experience Template (correct HTML, no stray closing tags inside content) ---
                    if not sp.get('experience'):
                        with st.expander("💼 Add Work Experience Template", expanded=False):
                            tpl_html = f"""
                            <div class='tpl-card'>
                                <div class='tpl-head'>Work Experience (STAR)</div>
                                <div class='tpl-tags'>
                                    <span class='tpl-tag'>{role_for_tpl}</span>
                                    <span class='tpl-tag'>{role_skills}</span>
                                </div>
                                <div class='tpl-pre'>
                    [Job Title] — [Company], [City] | [MMM YYYY] – [MMM YYYY or Present]
                    Scope: Owned [area/scope]; tools: [{role_skills}]
                    Impact: Achieved &lt;metric/value&gt; by &lt;action&gt.

                    • Led &lt;project/feature&gt; using {role_skills}; increased &lt;KPI&gt; by &lt;X%&gt;.
                    • Implemented &lt;solution&gt; that reduced &lt;time/cost&gt; by &lt;X%&gt;.
                    • Collaborated with &lt;team/stakeholders&gt; to deliver &lt;outcome&gt;; validated via &lt;metric&gt;.
                    • Documented results and created &lt;artifact/report&gt; for visibility.
                                </div>
                                <div class='tpl-tips'>💡 Tip: Start bullets with action verbs and end with measurable outcomes.</div>
                            </div>
                            """
                            st.markdown(tpl_html, unsafe_allow_html=True)

                    # --- Summary Template (same fix) ---
                    if not sp.get('summary'):
                        with st.expander("🧾 Add Summary / Objective Template", expanded=False):
                            tpl2_html = f"""
                            <div class='tpl-card'>
                                <div class='tpl-head'>Professional Summary</div>
                                <div class='tpl-tags'>
                                    <span class='tpl-tag'>{role_for_tpl}</span>
                                    <span class='tpl-tag'>{role_skills}</span>
                                </div>
                                <div class='tpl-pre'>
                    Aspiring {role_for_tpl} with hands-on experience in {role_skills}. Strong foundation in data-driven problem solving and delivering measurable results.
                    Looking to contribute to &lt;team/company&gt; by &lt;how you will add value&gt;, backed by &lt;projects/certifications&gt;.
                                </div>
                                <div class='tpl-tips'>💡 Tip: Keep it concise (2–3 sentences); include strengths and target role.</div>
                            </div>
                            """
                            st.markdown(tpl2_html, unsafe_allow_html=True)



                    st.markdown("</div>", unsafe_allow_html=True)

                # Role Alignment Analysis (moved below Top Suggestions)
                if 'kw_role_alignment' in components:
                    st.markdown("""
                    <style>
                    .role-wrap { background: linear-gradient(145deg, #0b1221, #151c30); border:1px solid rgba(255,255,255,0.06); border-radius:20px; padding:16px 18px; margin: 10px 0 20px; box-shadow:0 10px 30px rgba(0,0,0,.35); }
                    .role-head { display:flex; flex-direction:column; gap:4px; }
                    .role-title { color:#E6EAF3; font-size:20px; font-weight:800; margin:0; }
                    .role-sub { color:#9AA4B2; font-size:13px; }
                    .chipset { display:flex; gap:8px; flex-wrap:wrap; margin-top:10px; }
                    .chip { display:inline-flex; align-items:center; gap:.45rem; padding:.5rem .75rem; border-radius:14px; font-size:12px; font-weight:800; border:1px solid rgba(255,255,255,.08); color:#E6EAF3; background: linear-gradient(145deg, rgba(255,255,255,.06), rgba(255,255,255,.03)); transition: transform .15s ease, box-shadow .15s ease; }
                    .chip:hover { transform: translateY(-1px); box-shadow: 0 8px 18px rgba(99,102,241,.18); }
                    .high { background: linear-gradient(145deg, rgba(16,185,129,.25), rgba(16,185,129,.10)); border-color: rgba(16,185,129,.35); color:#CFFAE3; }
                    .med { background: linear-gradient(145deg, rgba(45,212,191,.22), rgba(34,197,94,.10)); border-color: rgba(45,212,191,.35); color:#D1FAF0; }
                    .low { background: linear-gradient(145deg, rgba(148,163,184,.16), rgba(148,163,184,.06)); border-color: rgba(148,163,184,.35); color:#E5E7EB; }
                    .tag { display:inline-flex; align-items:center; gap:.35rem; padding:.35rem .6rem; border-radius:999px; font-size:12px; font-weight:800; color:#9EC5FF; border:1px solid rgba(59,130,246,.35); background: rgba(59,130,246,.10); }
                    </style>
                    """, unsafe_allow_html=True)

                    role_label = ''
                    if role == 'Auto-detect':
                        auto_role = components.get('kw_role_alignment_role')
                        if auto_role:
                            role_label = f"<span class='tag'>Auto-detected: {auto_role}</span>"
                    else:
                        role_label = f"<span class='tag'>Target: {role}</span>"

                    top_roles = components.get('kw_role_alignment_top') or []
                    icon_map = { 'Software Engineer':'💻', 'Data Analyst':'📊', 'Machine Learning Engineer':'🤖', 'Web Developer':'🌐' }

                    chips = []
                    for r in top_roles:
                        role_name = r.get('role') or 'Role'
                        score8 = r.get('score') or 0
                        level = 'high' if score8 >= 6 else ('med' if score8 >= 4 else 'low')
                        icon = icon_map.get(role_name, '🧩')
                        title = ', '.join(r.get('keywords', []))
                        chips.append(f"<span class='chip {level}' title='{title}'>{icon} {role_name} • {score8}/8</span>")

                    st.markdown(
                        f"""
                        <div class='role-wrap fade-in'>
                            <div class='role-head'>
                                <div class='role-title'>Role Alignment Analysis</div>
                                <div class='role-sub'>Based on extracted skills and keyword matches. {role_label}</div>
                            </div>
                            <div class='chipset'>{''.join(chips)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Divider after Role Alignment Analysis
                st.markdown("<hr style='margin: 40px 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);' />", unsafe_allow_html=True)

                # Cache resume context for chat so first turn has context
                try:
                    st.session_state['resume_context'] = build_resume_context(resume_data)
                except Exception:
                    st.session_state['resume_context'] = None

                # Defer chat rendering to bottom of page
                st.session_state['render_chat_at_bottom'] = True
                
                # Divider before job search section
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
                
                # Job search - Improved Section
                st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)
                st.markdown("""
                <style>
                @keyframes slideInLeft {{
                    0% {{ 
                        opacity: 0;
                        transform: translateX(-20px);
                    }}
                    100% {{ 
                        opacity: 1;
                        transform: translateX(0px);
                    }}
                }}
                
                .job-search-section {{
                    background: linear-gradient(135deg, #1A1F3A 0%, #242F5C 50%, #1A1F3A 100%);
                    border: 1.5px solid rgba(99, 102, 241, 0.3);
                    border-radius: 20px;
                    padding: 40px;
                    margin: 50px 0 40px 0;
                    box-shadow: 0 10px 40px rgba(99, 102, 241, 0.12), 0 0 20px rgba(99, 102, 241, 0.05);
                    position: relative;
                    overflow: hidden;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    animation: cardSlideIn 0.6s ease-out;
                }}
                
                .job-search-section:hover {{
                    border-color: rgba(139, 92, 246, 0.4);
                    box-shadow: 0 15px 50px rgba(139, 92, 246, 0.15), 0 0 30px rgba(99, 102, 241, 0.1);
                    background: linear-gradient(135deg, #242F5C 0%, #2D3A6B 50%, #242F5C 100%);
                }}
                
                .search-title {{
                    font-size: 28px;
                    font-weight: 800;
                    background: linear-gradient(135deg, #FFFFFF 0%, #A78BFA 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin-bottom: 28px;
                    animation: slideInLeft 0.6s ease-out;
                    letter-spacing: -0.5px;
                }}
                </style>
                <div class="job-search-section">
                    <div class="search-title">💼 Find Your Next Opportunity</div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    location_input = st.text_input("📍 Location", placeholder="Enter preferred location (leave blank for remote)", key="search_location")
                with col2:
                    # Build default keywords from role alignment + top skills (tech-focused, max 3 terms)
                    def _default_keywords(skills_list, comps):
                        role_name = None
                        try:
                            role_name = (comps.get('kw_role_alignment_role') or None) if comps else None
                            if not role_name and comps and comps.get('kw_role_alignment_top'):
                                role_name = comps['kw_role_alignment_top'][0].get('role')
                        except Exception:
                            role_name = None
                        tech_stop = {"sales","marketing","operations","hr","human resources","business development"}
                        sk = [s for s in (skills_list or []) if isinstance(s, str) and s.strip() and s.strip().lower() not in tech_stop]
                        # prefer skills that look technical (letters/digits and common tech separators)
                        def _is_tech(x:str):
                            t=x.lower()
                            return any(k in t for k in ["python","java","react","node","sql","ml","data","django","flask","frontend","backend","devops","cloud","android","ios","c++","c#","go","rust","pandas","numpy","matplotlib","seaborn","streamlit"])
                        tech_sk = [s for s in sk if _is_tech(s)] or sk
                        parts = ([role_name] if role_name else []) + tech_sk
                        parts = [p for p in parts if p][:3]
                        return ", ".join(parts)
                    default_kw = _default_keywords(skills, components)
                    keywords_input = st.text_input("🧠 Skills/Keywords", value=default_kw, placeholder="e.g., Python, React, SQL", key="search_keywords")
                with col3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    search_button = st.button("🔍 Search", use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

                # Divider after Job Search header
                st.markdown("<hr style='margin: 40px 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);' />", unsafe_allow_html=True)
                
                # Display dual-section recommendations (Jooble + Internshala)
                if skills:
                    # Get predicted category for job filtering
                    predicted_cat = resume_data.get('predicted_category')
                    if predicted_cat:
                        st.info(f"🎯 Showing jobs relevant to: **{predicted_cat}**")
                    display_job_recommendations_dual(skills, keywords_input, location_input or "India", predicted_cat)
                
                # Category-based course recommendations
                predicted_cat = resume_data.get('predicted_category')
                course_list = []
                
                if predicted_cat:
                    # Get courses based on ML predicted category
                    category_courses = get_courses_by_category(predicted_cat)
                    course_list.extend(category_courses)
                
                # Fallback: skill-based recommendations if no category or no courses
                if not course_list:
                    if any(skill.lower() in ['python', 'pandas', 'numpy', 'machine learning', 'data analysis'] for skill in skills):
                        course_list.extend(ds_course)
                    if any(skill.lower() in ['html', 'css', 'javascript', 'react'] for skill in skills):
                        course_list.extend(web_course)
                    if any(skill.lower() in ['kotlin', 'java', 'android'] for skill in skills):
                        course_list.extend(android_course)
                    if any(skill.lower() in ['swift', 'ios'] for skill in skills):
                        course_list.extend(ios_course)
                    if any(skill.lower() in ['figma', 'ui/ux', 'prototyping'] for skill in skills):
                        course_list.extend(uiux_course)
                
                if course_list:
                    # Divider before courses section
                    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
                    recommended_courses = course_recommender(course_list)
                
                # Save to database (only once per resume upload)
                # Use a combination of resume file identity + email to prevent duplicates
                if resume_data.get('name') and resume_data.get('email'):
                    # Create a unique key based on resume identity and user email
                    resume_id = st.session_state.get('resume_id', '')
                    user_email = resume_data.get('email', '')
                    resume_db_key = f"db_saved_{hash(resume_id + user_email)}"
                    
                    # Only insert if we haven't saved this specific resume for this user
                    if resume_id and not st.session_state.get(resume_db_key, False):
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
                        success = db_manager.insert_user_data(
                            name=resume_data['name'],
                            email=resume_data['email'],
                            res_score=score,
                            timestamp=timestamp,
                            no_of_pages=1,  # Default
                            reco_field="General",
                            cand_level="Intermediate",
                            skills=skills,
                            recommended_skills=[],
                            courses=recommended_courses if 'recommended_courses' in locals() else []
                        )
                        if success:
                            # Mark this resume as saved to prevent duplicates on subsequent reruns
                            st.session_state[resume_db_key] = True

        # Divider before AI chat section
        st.markdown('<hr class="section-divider-lg">', unsafe_allow_html=True)

        # Render chat at the very bottom
        if st.session_state.get('render_chat_at_bottom'):
            # === STYLE BLOCK ===
            st.markdown("""
            <style>
            /* === CONTAINER === */
            .assistant-container {
                background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(0,0,0,0.25));
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 18px;
                padding: 28px 36px;
                margin-top: 50px;
                margin-bottom: 40px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.35);
                transition: all 0.3s ease;
            }
            .assistant-container:hover {
                box-shadow: 0 10px 32px rgba(0,0,0,0.45);
            }

            /* === HEADER === */
            .assistant-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 14px;
                padding: 14px 18px;
                margin-bottom: 15px;
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02), 0 6px 20px rgba(0,0,0,0.25);
            }
            .assistant-title {
                display: flex;
                align-items: center;
                gap: 10px;
                font-weight: 700;
                font-size: 1.25rem;
                color: #e5e7eb;
                letter-spacing: 0.3px;
            }
            .assistant-status {
                color: #22c55e;
                font-size: 0.9rem;
                animation: pulse 1.8s infinite;
            }
            @keyframes pulse { 0%{opacity:1;} 50%{opacity:0.6;} 100%{opacity:1;} }

            /* === CHAT AREA === */
            .chat-scroll {
                max-height: 500px;
                overflow-y: auto;
                padding: 15px;
                background: rgba(255,255,255,0.02);
                border-radius: 14px;
                margin-bottom: 16px;
            }
            .chat-scroll::-webkit-scrollbar {
                width: 6px;
            }
            .chat-scroll::-webkit-scrollbar-thumb {
                background: rgba(255,255,255,0.08);
                border-radius: 10px;
            }

            /* === MESSAGE BUBBLES === */
            .message-container {
                display: flex;
                flex-direction: column;
                margin-bottom: 12px;
            }
            .message-user { align-items: flex-end; }
            .message-assistant { align-items: flex-start; }
            .message-bubble {
                padding: 12px 16px;
                border-radius: 16px;
                max-width: 80%;
                word-wrap: break-word;
                font-size: 0.95rem;
                line-height: 1.5;
                animation: fadeIn 0.3s ease-in-out;
            }
            .user {
                background: linear-gradient(135deg, #6366f1, #0ea5e9);
                color: #fff;
                border-bottom-right-radius: 4px;
                text-align: right;
                margin-left: auto;
            }
            .assistant {
                background: rgba(255,255,255,0.08);
                color: #e2e8f0;
                border-bottom-left-radius: 4px;
                text-align: left;
            }
            @keyframes fadeIn { from {opacity: 0; transform: translateY(6px);} to {opacity: 1; transform: translateY(0);} }

            .message-time {
                font-size: 0.75rem;
                color: rgba(255,255,255,0.4);
                margin-top: 2px;
            }

            /* === INPUT AREA === */
            .chat-input {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 16px;
                padding: 10px 14px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 8px;
            }
            .chat-input input {
                background: transparent;
                color: white;
                border: none;
                width: 100%;
                outline: none;
            }
            .stButton>button {
                border-radius: 12px !important;
                background: linear-gradient(90deg, #7c3aed, #2dd4bf);
                border: none;
                color: white;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                transform: scale(1.05);
                box-shadow: 0 0 12px rgba(124,58,237,0.4);
            }

            /* === TYPING ANIMATION === */
            .typing-indicator {
                display: flex;
                align-items: center;
                gap: 8px;
                color: rgba(255,255,255,0.7);
                font-size: 0.9rem;
            }
            .typing-dots {
                display: flex;
                gap: 4px;
            }
            .typing-dot {
                width: 6px;
                height: 6px;
                background: #9ca3af;
                border-radius: 50%;
                animation: blink 1.4s infinite both;
            }
            .typing-dot:nth-child(2){animation-delay:0.2s;}
            .typing-dot:nth-child(3){animation-delay:0.4s;}
            @keyframes blink { 0%{opacity:0.2;} 20%{opacity:1;} 100%{opacity:0.2;} }
            </style>
            """, unsafe_allow_html=True)

            # === MAIN ASSISTANT CONTAINER START ===
            st.markdown('<div class="assistant-container">', unsafe_allow_html=True)

            # HEADER
            st.markdown("""
            <div class="assistant-header">
                <div class="assistant-title">
                    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712100.png" width="36" alt="Assistant">
                    InternHunt Assistant
                </div>
                <div class="assistant-status">🟢 Online</div>
            </div>
            """, unsafe_allow_html=True)

            # CHAT STYLE / OPTIONS
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            with col1:
                chat_style = st.selectbox("Chat Style", ["Concise", "Detailed", "Short"], index=0, key="chat_style", label_visibility="collapsed")
            with col2:
                st.session_state['chat_use_context'] = st.checkbox("Use resume context", value=True, key="chat_use_ctx")
            with col3:
                if st.button("🗑️ Clear", key="chat_clear", help="Clear chat history"):
                    st.session_state['chat_messages'] = []
                    st.toast("Chat cleared!")
                    st.rerun()
            with col4:
                if st.button("🔥 Test", key="chat_test", help="Test AI connection"):
                    with st.spinner("Testing AI connection..."):
                        try:
                            health = check_gemini_health()
                            if health['status'] == 'healthy' and health['api_key_configured']:
                                _ = chat_gemini([{ "role": "user", "content": "Hello"}], None, "Respond with 'Ready to help!'")
                                st.success("AI connection working! 🚀")
                            else:
                                st.error(f"AI not ready: {health.get('error', 'Unknown error')}")
                        except Exception as e:
                            st.error(f"Failed to connect: {e}")

            # CHAT HISTORY
            st.markdown('<div class="chat-scroll">', unsafe_allow_html=True)
            import html
            if 'chat_messages' not in st.session_state:
                st.session_state['chat_messages'] = []
            for m in st.session_state['chat_messages'][-50:]:
                role = m.get('role', 'user')
                content = html.escape(m.get('content', '') or '').replace('\n', '<br>')
                timestamp = m.get('timestamp', '')
                if role == 'user':
                    st.markdown(f"""
                        <div class="message-container message-user">
                            <div class="message-bubble user">{content}</div>
                            <div class="message-time">{timestamp}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="message-container message-assistant">
                            <div class="message-bubble assistant">{content}</div>
                            <div class="message-time">{timestamp}</div>
                        </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # === CHAT INPUT ===
            left_pad, mid_col, right_pad = st.columns([1, 8, 1])
            with mid_col:
                st.markdown('<div class="chat-input">', unsafe_allow_html=True)
                with st.form("chat_form", clear_on_submit=True, border=False):
                    c_in1, c_in2 = st.columns([10, 1])
                    with c_in1:
                        user_text_value = st.text_input(
                            "Chat Input", 
                            placeholder="Ask me anything about your resume, career, or job search...", 
                            key="chat_text_input",
                            label_visibility="collapsed"
                        )
                    with c_in2:
                        send = st.form_submit_button("➤", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # === MESSAGE PROCESSING ===
            user_text = (user_text_value or "").strip() if send else None
            if user_text:
                timestamp = datetime.datetime.now().strftime("%H:%M")
                st.session_state['chat_messages'].append({
                    "role": "user",
                    "content": user_text,
                    "timestamp": timestamp
                })
                # Typing animation
                with st.spinner("🤖 Thinking..."):
                    typing_placeholder = st.empty()
                    typing_placeholder.markdown("""
                        <div class="message-container message-assistant">
                            <div class="message-bubble assistant typing-indicator">
                                <span>🤖 Thinking</span>
                                <div class="typing-dots">
                                    <div class="typing-dot"></div>
                                    <div class="typing-dot"></div>
                                    <div class="typing-dot"></div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    context = st.session_state.get('resume_context') if st.session_state.get('chat_use_context', True) else None
                    if chat_style == "Concise":
                        sys = "Be brief and friendly. Give 2-3 quick tips in plain language."
                    elif chat_style == "Detailed":
                        sys = "Give helpful advice in a conversational tone. Include 3-4 specific recommendations."
                    else:
                        sys = "Answer in 2-3 natural sentences like you're helping a friend."
                    try:
                        from dotenv import load_dotenv
                        load_dotenv(override=True)
                        reply = chat_gemini(
                            st.session_state['chat_messages'], 
                            resume_context=context, 
                            system_prompt=sys
                        )
                        typing_placeholder.empty()
                        if reply:
                            st.session_state['chat_messages'].append({
                                "role": "assistant",
                                "content": reply,
                                "timestamp": datetime.datetime.now().strftime("%H:%M")
                            })
                        st.rerun()
                    except Exception as e:
                        typing_placeholder.empty()
                        st.session_state['chat_messages'].append({
                            "role": "assistant",
                            "content": f"⚠️ {str(e)}",
                            "timestamp": datetime.datetime.now().strftime("%H:%M")
                        })
                        st.rerun()

            # === FOOTER ===
            st.markdown("""
            <hr style="opacity:0.1; margin:20px 0;">
            <p style="text-align:center; color:rgba(255,255,255,0.4); font-size:0.85rem;">
                💬 InternHunt Assistant — Ready to guide your career journey.
            </p>
            """, unsafe_allow_html=True)

            # Auto-scroll to latest message
            st.markdown("""
            <script>
                var chat = window.parent.document.querySelector('.chat-scroll');
                if (chat) { chat.scrollTop = chat.scrollHeight; }
            </script>
            """, unsafe_allow_html=True)

            # CLOSE CONTAINER
            st.markdown("</div>", unsafe_allow_html=True)
                
        elif choice == 'Admin':
            st.subheader(" Admin Dashboard")
            
            # Display user data
            user_data = db_manager.get_user_data(50)
            if user_data:
                df = pd.DataFrame(user_data, columns=[
                    'ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Pages',
                    'Predicted Field', 'User Level', 'Skills', 'Recommended Skills', 'Courses'
                ])
                st.dataframe(df)
                
                # Download link
                st.markdown(
                    get_table_download_link(df, "user_data.csv", " Download Data as CSV"),
                    unsafe_allow_html=True
                )
            else:
                st.info("No user data available.")
    
    # ============ FOOTER ============ 
    st.markdown(""" 
        <footer style="text-align: center; margin-top: 80px; font-size: 
    0.9rem; opacity: 0.7; font-family: 'Inter', sans-serif;
    color: #94a3b8; padding: 20px 0;">
                        © 2025 InternHunt • Crafted with ❤️ by Shubham, Abhinav, Pragya & Parmesh
                </footer> 
                """,unsafe_allow_html=True)

if __name__ == "__main__":
    main()
