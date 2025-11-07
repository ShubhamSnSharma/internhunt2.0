# CSS styles module for InternHunt - Professional UI Design System
import streamlit as st

class StyleManager:
    """Manages all CSS styles for the application with a modern, professional design system"""
    
    # Professional Color Palette - Enhanced Purple & Dark Theme
    COLORS = {
        # Primary Colors - Modern Purple-Indigo Gradient
        'primary': '#6366F1',          # Indigo-500
        'primary_light': '#818CF8',     # Indigo-400
        'primary_dark': '#4F46E5',      # Indigo-600
        'primary_gradient': 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)',
        
        # Secondary Purple Tones
        'purple_600': '#7C3AED',        # Purple-600
        'purple_500': '#A78BFA',        # Purple-400
        'purple_dark': '#5B21B6',       # Purple-800
        
        # Accent Colors - Vibrant Green
        'accent': '#10B981',            # Emerald-500
        'accent_light': '#34D399',      # Emerald-400
        'accent_dark': '#059669',       # Emerald-600
        
        # Neutral Colors - Sophisticated Grays
        'gray_50': '#F9FAFB',
        'gray_100': '#F3F4F6',
        'gray_200': '#E5E7EB',
        'gray_300': '#D1D5DB',
        'gray_400': '#9CA3AF',
        'gray_500': '#6B7280',
        'gray_600': '#4B5563',
        'gray_700': '#374151',
        'gray_800': '#1F2937',
        'gray_900': '#111827',
        
        # Dark Theme Colors - Deep Purple-Tinted
        'dark_bg': '#0D1429',           # Very Dark Blue-Purple
        'dark_surface': '#1A1F3A',      # Dark Blue-Purple Surface
        'dark_card': '#242F5C',         # Card Background with Purple tint
        'dark_border': '#3A4570',       # Border Purple-tint
        
        # Light Theme Colors
        'light_bg': '#FFFFFF',
        'light_surface': '#F8FAFC',     # Slate-50
        'light_card': '#FFFFFF',
        'light_border': '#E2E8F0',      # Slate-200
        
        # Status Colors
        'success': '#10B981',           # Emerald-500
        'warning': '#F59E0B',           # Amber-500
        'error': '#EF4444',             # Red-500
        'info': '#3B82F6',              # Blue-500
    }
    
    @classmethod
    def apply_global_styles(cls):
        """Apply modern global CSS styles with professional design system"""
        st.markdown(f"""
        <style>
        /* Base Styles */
        :root {{
            --primary: {cls.COLORS['primary']};
            --primary-light: {cls.COLORS['primary_light']};
            --primary-dark: {cls.COLORS['primary_dark']};
            --accent: {cls.COLORS['accent']};
            --dark-bg: {cls.COLORS['dark_bg']};
            --dark-surface: {cls.COLORS['dark_surface']};
            --dark-card: {cls.COLORS['dark_card']};
            --dark-border: {cls.COLORS['dark_border']};
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--text-primary) !important;
            background-color: var(--dark-bg) !important;
            margin: 0;
            padding: 0;
        }}
        
        /* Force dark theme on all Streamlit elements */
        .stApp, .stApp > div, .main, .block-container, .stApp > div > div > div > div > section > div > div > div > div,
        .stApp > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div,
        .stApp > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div {{
            background-color: var(--dark-bg) !important;
            color: var(--text-primary) !important;
        }}
        
        /* Ensure all text is visible */
        .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, 
        .stMarkdown h5, .stMarkdown h6, .stMarkdown li, .stMarkdown ol, .stMarkdown ul, .stMarkdown table,
        .stAlert, .stAlert p, .stAlert h1, .stAlert h2, .stAlert h3, .stAlert h4,
        .stAlert h5, .stAlert h6, .stAlert li, .stAlert ol, .stAlert ul, .stAlert table {{
            color: var(--text-primary) !important;
        }}
        
        /* Style file uploader */
        .stFileUploader > div > div > div > button {{
            background: var(--primary) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s ease !important;
        }}
        
        .stFileUploader > div > div > div > button:hover {{
            background: var(--primary-light) !important;
            transform: translateY(-1px) !important;
        }} font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        /* Streamlit Container Adjustments */
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1100px;
            padding-left: 1.25rem;
            padding-right: 1.25rem;
        }}
        
        /* Hide Streamlit Elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .stDeployButton {{display: none;}}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {StyleManager.COLORS['gray_100']};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {StyleManager.COLORS['gray_300']};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {StyleManager.COLORS['gray_400']};
        }}
        
        /* Professional Typography Scale */
        .typography-h1 {{
            font-size: 3rem;
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }}
        
        .typography-h2 {{
            font-size: 2.25rem;
            font-weight: 700;
            line-height: 1.2;
            letter-spacing: -0.01em;
        }}
        
        .typography-h3 {{
            font-size: 1.875rem;
            font-weight: 600;
            line-height: 1.3;
        }}
        
        .typography-body-large {{
            font-size: 1.125rem;
            line-height: 1.6;
            font-weight: 400;
        }}
        
        .typography-body {{
            font-size: 1rem;
            line-height: 1.6;
            font-weight: 400;
        }}
        
        .typography-caption {{
            font-size: 0.875rem;
            line-height: 1.4;
            font-weight: 500;
        }}
        
        /* Professional Card System */
        .pro-card {{
            background: {StyleManager.COLORS['light_card']};
            border: 1px solid {StyleManager.COLORS['light_border']};
            border-radius: 16px;
            padding: 24px;
            margin: 16px 0;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            transition: all 0.2s ease-in-out;
        }}
        
        .pro-card:hover {{
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transform: translateY(-2px);
        }}
        
        .pro-card-header {{
            display: flex;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid {StyleManager.COLORS['gray_200']};
        }}
        
        .pro-card-icon {{
            width: 40px;
            height: 40px;
            background: {StyleManager.COLORS['primary_gradient']};
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            font-size: 18px;
        }}
        
        .pro-card-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: {StyleManager.COLORS['gray_900']};
            margin: 0;
        }}
        
        /* Professional Button System */
        .pro-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 12px 24px;
            font-size: 0.875rem;
            font-weight: 600;
            border-radius: 12px;
            border: none;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s ease-in-out;
            gap: 8px;
        }}
        
        .pro-btn-primary {{
            background: {StyleManager.COLORS['primary_gradient']};
            color: white;
            box-shadow: 0 1px 2px 0 rgba(79, 70, 229, 0.05);
        }}
        
        .pro-btn-primary:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px 0 rgba(79, 70, 229, 0.15);
        }}
        
        .pro-btn-secondary {{
            background: {StyleManager.COLORS['gray_100']};
            color: {StyleManager.COLORS['gray_700']};
            border: 1px solid {StyleManager.COLORS['gray_300']};
        }}
        
        .pro-btn-secondary:hover {{
            background: {StyleManager.COLORS['gray_200']};
            border-color: {StyleManager.COLORS['gray_400']};
        }}
        
        .pro-btn-success {{
            background: {StyleManager.COLORS['success']};
            color: white;
        }}
        
        .pro-btn-success:hover {{
            background: {StyleManager.COLORS['accent_dark']};
            transform: translateY(-1px);
        }}
        
        /* Professional Badge System */
        .pro-badge {{
            display: inline-flex;
            align-items: center;
            padding: 6px 12px;
            font-size: 0.75rem;
            font-weight: 600;
            border-radius: 8px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .pro-badge-primary {{
            background: rgba(79, 70, 229, 0.1);
            color: {StyleManager.COLORS['primary_dark']};
        }}
        
        .pro-badge-success {{
            background: rgba(16, 185, 129, 0.1);
            color: {StyleManager.COLORS['accent_dark']};
        }}
        
        .pro-badge-warning {{
            background: rgba(245, 158, 11, 0.1);
            color: #D97706;
        }}
        
        /* Professional Alert System */
        .pro-alert {{
            padding: 16px;
            border-radius: 12px;
            margin: 16px 0;
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }}
        
        .pro-alert-info {{
            background: rgba(59, 130, 246, 0.05);
            border: 1px solid rgba(59, 130, 246, 0.2);
            color: #1E40AF;
        }}
        
        .pro-alert-success {{
            background: rgba(16, 185, 129, 0.05);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: #047857;
        }}
        
        .pro-alert-warning {{
            background: rgba(245, 158, 11, 0.05);
            border: 1px solid rgba(245, 158, 11, 0.2);
            color: #92400E;
        }}
        
        .pro-alert-error {{
            background: rgba(239, 68, 68, 0.05);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #DC2626;
        }}
        
        /* Layout Improvements */
        .pro-container {{
            max-width: 100%;
            margin: 0 auto;
            padding: 0 16px;
        }}
        
        .pro-grid {{
            display: grid;
            gap: 24px;
        }}
        
        .pro-grid-2 {{
            grid-template-columns: repeat(2, 1fr);
        }}
        
        .pro-grid-3 {{
            grid-template-columns: repeat(3, 1fr);
        }}
        
        @media (max-width: 768px) {{
            .pro-grid-2, .pro-grid-3 {{
                grid-template-columns: 1fr;
            }}
            
            .main .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    @classmethod
    def apply_theme_styles(cls, theme_mode: str):
        """Apply professional theme-specific styles"""
        if theme_mode == "dark":
            st.markdown(f"""
            <style>
            /* Dark Theme - Professional */
            .stApp {{
                background-color: {StyleManager.COLORS['dark_bg']};
                color: #F1F5F9;
            }}
            
            /* Dark Theme Cards */
            .pro-card {{
                background: {StyleManager.COLORS['dark_surface']};
                border-color: {StyleManager.COLORS['dark_border']};
                color: #F1F5F9;
            }}
            
            .pro-card:hover {{
                background: #293548;
                box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            }}
            
            .pro-card-header {{
                border-bottom-color: {StyleManager.COLORS['dark_border']};
            }}
            
            .pro-card-title {{
                color: #F1F5F9;
            }}
            
            /* Dark Theme Typography */
            .typography-h1, .typography-h2, .typography-h3 {{
                color: #F8FAFC;
            }}
            
            /* Dark Theme Buttons */
            .pro-btn-secondary {{
                background: {StyleManager.COLORS['dark_card']};
                color: #F1F5F9;
                border-color: {StyleManager.COLORS['dark_border']};
            }}
            
            .pro-btn-secondary:hover {{
                background: {StyleManager.COLORS['dark_border']};
                border-color: #64748B;
            }}
            
            /* Dark Theme Form Elements */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > select {{
                background-color: {StyleManager.COLORS['dark_surface']};
                border: 1px solid {StyleManager.COLORS['dark_border']};
                color: #F1F5F9;
            }}
            
            /* Dark Theme Sidebar */
            .css-1d391kg {{
                background-color: {StyleManager.COLORS['dark_surface']};
            }}
            
            /* Dark Theme Scrollbar */
            ::-webkit-scrollbar-track {{
                background: {StyleManager.COLORS['dark_surface']};
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: {StyleManager.COLORS['dark_border']};
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: #64748B;
            }}
            </style>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <style>
            /* Light Theme - Professional */
            .stApp {{
                background: linear-gradient(135deg, {StyleManager.COLORS['light_bg']} 0%, {StyleManager.COLORS['light_surface']} 100%);
                color: {StyleManager.COLORS['gray_900']};
            }}
            
            /* Light Theme Cards */
            .pro-card {{
                background: {StyleManager.COLORS['light_card']};
                border-color: {StyleManager.COLORS['light_border']};
                color: {StyleManager.COLORS['gray_900']};
            }}
            
            .pro-card:hover {{
                background: #FFFFFF;
                box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            }}
            
            /* Light Theme Typography */
            .typography-h1, .typography-h2, .typography-h3 {{
                color: {StyleManager.COLORS['gray_900']};
            }}
            
            /* Light Theme Form Elements */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > select {{
                background-color: {StyleManager.COLORS['light_card']};
                border: 1px solid {StyleManager.COLORS['light_border']};
                color: {StyleManager.COLORS['gray_900']};
            }}
            
            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus {{
                border-color: {StyleManager.COLORS['primary']};
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
            }}
            
            /* Light Theme Sidebar */
            .css-1d391kg {{
                background-color: {StyleManager.COLORS['light_surface']};
            }}
            </style>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def get_skills_styles():
        """Get professional CSS styles for skills display"""
        return f"""
        <style>
        /* Professional Skills Display */
        .skills-header {{
            display: flex;
            align-items: center;
            margin: 32px 0 24px 0;
            padding: 0 0 16px 0;
            border-bottom: 2px solid {StyleManager.COLORS['primary']};
            position: relative;
        }}
        
        .skills-header::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 60px;
            height: 2px;
            background: {StyleManager.COLORS['primary_gradient']};
        }}
        
        .skills-header-icon {{
            width: 48px;
            height: 48px;
            background: {StyleManager.COLORS['primary_gradient']};
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 16px;
            font-size: 20px;
            color: white;
        }}
        
        .skills-header-text {{
            font-size: 1.5rem;
            font-weight: 700;
            color: inherit;
            margin: 0;
            letter-spacing: -0.01em;
        }}
        
        .skills-container {{
            margin-top: 24px;
            padding: 0;
        }}
        
        .skill-section {{
            margin-bottom: 32px;
        }}
        
        .skill-category {{
            display: flex;
            align-items: center;
            margin: 0 0 16px 0;
            padding: 0 0 12px 0;
            font-weight: 600;
            font-size: 1.125rem;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        }}
        
        .category-icon {{
            font-size: 18px;
            margin-right: 12px;
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, {StyleManager.COLORS['gray_100']} 0%, {StyleManager.COLORS['gray_200']} 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .skills-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 24px;
        }}
        
        .skill-tag {{
            display: inline-flex;
            align-items: center;
            padding: 10px 16px;
            border-radius: 12px;
            font-size: 0.875rem;
            font-weight: 600;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: default;
            position: relative;
            overflow: hidden;
        }}
        
        .skill-tag::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }}
        
        .skill-tag:hover::before {{
            left: 100%;
        }}
        
        /* Skill Category Colors */
        .tech-skill {{
            background: linear-gradient(135deg, {StyleManager.COLORS['primary']} 0%, {StyleManager.COLORS['primary_light']} 100%);
            color: white;
            border: none;
        }}
        
        .tech-skill:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 25px -8px {StyleManager.COLORS['primary']};
        }}
        
        .hardware-skill {{
            background: linear-gradient(135deg, {StyleManager.COLORS['accent']} 0%, {StyleManager.COLORS['accent_light']} 100%);
            color: white;
            border: none;
        }}
        
        .hardware-skill:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 25px -8px {StyleManager.COLORS['accent']};
        }}
        
        .soft-skill {{
            background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
            color: white;
            border: none;
        }}
        
        .soft-skill:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 25px -8px #8B5CF6;
        }}
        
        .data-skill {{
            background: linear-gradient(135deg, #F59E0B 0%, #FDE047 100%);
            color: #92400E;
            border: none;
        }}
        
        .data-skill:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 25px -8px #F59E0B;
        }}
        
        .design-skill {{
            background: linear-gradient(135deg, #EC4899 0%, #F472B6 100%);
            color: white;
            border: none;
        }}
        
        .design-skill:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 25px -8px #EC4899;
        }}
        
        .business-skill {{
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            color: white;
            border: none;
        }}
        
        .business-skill:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 25px -8px #6366F1;
        }}
        
        .other-skill {{
            background: linear-gradient(135deg, {StyleManager.COLORS['gray_400']} 0%, {StyleManager.COLORS['gray_500']} 100%);
            color: white;
            border: none;
        }}
        
        .other-skill:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 25px -8px {StyleManager.COLORS['gray_400']};
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .skills-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }}
            
            .skills-header-icon {{
                margin-right: 0;
            }}
            
            .skill-tag {{
                font-size: 0.8rem;
                padding: 8px 12px;
            }}
        }}
        </style>
        """
    
    @staticmethod
    def get_job_listing_styles():
        """Get professional CSS styles for job listings"""
        return f"""
        <style>
        /* Professional Job Listing Cards */
        .job-listing {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .job-listing::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: {StyleManager.COLORS['primary_gradient']};
        }}
        
        .job-listing:hover {{
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(79, 70, 229, 0.3);
            transform: translateY(-4px);
            box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.25);
        }}
        
        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }}
        
        .job-title {{
            font-size: 1.375rem;
            font-weight: 700;
            color: #F8FAFC;
            margin: 0 0 8px 0;
            line-height: 1.3;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .job-title-icon {{
            width: 40px;
            height: 40px;
            background: {StyleManager.COLORS['primary_gradient']};
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            color: white;
        }}
        
        .job-company {{
            font-size: 1rem;
            color: {StyleManager.COLORS['gray_400']};
            font-weight: 500;
            margin-bottom: 4px;
        }}
        
        .job-location {{
            font-size: 0.875rem;
            color: {StyleManager.COLORS['gray_500']};
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .job-info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin: 20px 0;
        }}
        
        .job-info-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 16px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .job-info-icon {{
            width: 32px;
            height: 32px;
            background: {StyleManager.COLORS['primary_gradient']};
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: white;
        }}
        
        .job-info-content {{
            flex: 1;
        }}
        
        .job-info-label {{
            font-size: 0.75rem;
            font-weight: 600;
            color: {StyleManager.COLORS['gray_400']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 2px;
        }}
        
        .job-info-value {{
            font-size: 0.875rem;
            color: #F1F5F9;
            font-weight: 500;
        }}
        
        .job-description {{
            color: {StyleManager.COLORS['gray_300']};
            line-height: 1.6;
            margin: 20px 0;
            font-size: 0.875rem;
        }}
        
        .job-skills {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 20px 0;
        }}
        
        .job-skill-tag {{
            background: rgba(79, 70, 229, 0.2);
            color: {StyleManager.COLORS['primary_light']};
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 600;
            border: 1px solid rgba(79, 70, 229, 0.3);
        }}
        
        .job-actions {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 24px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .job-salary {{
            font-size: 1.125rem;
            font-weight: 700;
            color: {StyleManager.COLORS['success']};
        }}
        
        .apply-button {{
            background: {StyleManager.COLORS['primary_gradient']};
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 12px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .apply-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4);
        }}
        
        .apply-button:active {{
            transform: translateY(0);
        }}
        
        .job-match-score {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: {StyleManager.COLORS['success']};
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .separator {{
            height: 1px;
            background: linear-gradient(
                to right, 
                transparent, 
                rgba(79, 70, 229, 0.3) 20%, 
                rgba(79, 70, 229, 0.6) 50%, 
                rgba(79, 70, 229, 0.3) 80%, 
                transparent
            );
            margin: 32px 0;
        }}
        
        /* Light theme adjustments */
        [data-theme="light"] .job-listing {{
            background: white;
            border-color: {StyleManager.COLORS['light_border']};
        }}
        
        [data-theme="light"] .job-listing:hover {{
            background: {StyleManager.COLORS['light_surface']};
            box-shadow: 0 20px 40px -12px rgba(79, 70, 229, 0.15);
        }}
        
        [data-theme="light"] .job-title {{
            color: {StyleManager.COLORS['gray_900']};
        }}
        
        [data-theme="light"] .job-info-item {{
            background: {StyleManager.COLORS['light_surface']};
            border-color: {StyleManager.COLORS['light_border']};
        }}
        
        [data-theme="light"] .job-info-value {{
            color: {StyleManager.COLORS['gray_700']};
        }}
        
        [data-theme="light"] .job-description {{
            color: {StyleManager.COLORS['gray_600']};
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .job-info-grid {{
                grid-template-columns: 1fr;
            }}
            
            .job-header {{
                flex-direction: column;
                gap: 12px;
            }}
            
            .job-actions {{
                flex-direction: column;
                gap: 12px;
                align-items: stretch;
            }}
            
            .apply-button {{
                justify-content: center;
            }}
        }}
        </style>
        """
    
    @staticmethod
    def get_animation_styles():
        """Get professional CSS animation styles"""
        return f"""
        <style>
        /* Professional Animations */
        @keyframes fadeSlideIn {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes fadeSlideInLeft {{
            from {{
                opacity: 0;
                transform: translateX(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        @keyframes fadeSlideInRight {{
            from {{
                opacity: 0;
                transform: translateX(30px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        @keyframes gentleGlow {{
            0%, 100% {{
                box-shadow: 0 0 20px rgba(79, 70, 229, 0.1);
            }}
            50% {{
                box-shadow: 0 0 30px rgba(79, 70, 229, 0.2);
            }}
        }}
        
        @keyframes shimmer {{
            0% {{
                background-position: -1000px 0;
            }}
            100% {{
                background-position: 1000px 0;
            }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{
                opacity: 1;
            }}
            50% {{
                opacity: 0.6;
            }}
        }}
        
        @keyframes bounce {{
            0%, 20%, 53%, 80%, 100% {{
                transform: translate3d(0, 0, 0);
            }}
            40%, 43% {{
                transform: translate3d(0, -8px, 0);
            }}
            70% {{
                transform: translate3d(0, -4px, 0);
            }}
            90% {{
                transform: translate3d(0, -2px, 0);
            }}
        }}
        
        /* Animation Classes */
        .animate-fade-in {{
            animation: fadeSlideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .animate-fade-in-left {{
            animation: fadeSlideInLeft 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .animate-fade-in-right {{
            animation: fadeSlideInRight 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .animate-delay-100 {{
            animation-delay: 0.1s;
        }}
        
        .animate-delay-200 {{
            animation-delay: 0.2s;
        }}
        
        .animate-delay-300 {{
            animation-delay: 0.3s;
        }}
        
        .animate-delay-400 {{
            animation-delay: 0.4s;
        }}
        
        /* Header Animations */
        .animated-header {{
            animation: fadeSlideIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .animated-header:hover {{
            animation: gentleGlow 2s infinite;
        }}
        
        /* Shimmer Effect */
        .shimmer-effect {{
            position: relative;
            overflow: hidden;
        }}
        
        .shimmer-effect::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.1),
                transparent
            );
            animation: shimmer 2s infinite;
        }}
        
        /* Loading Animation */
        .loading-dots {{
            display: inline-flex;
            gap: 4px;
        }}
        
        .loading-dot {{
            width: 8px;
            height: 8px;
            background: {StyleManager.COLORS['primary']};
            border-radius: 50%;
            animation: pulse 1.4s ease-in-out infinite both;
        }}
        
        .loading-dot:nth-child(1) {{
            animation-delay: -0.32s;
        }}
        
        .loading-dot:nth-child(2) {{
            animation-delay: -0.16s;
        }}
        
        /* Hover Animations */
        .hover-lift {{
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .hover-lift:hover {{
            transform: translateY(-2px);
        }}
        
        .hover-scale {{
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .hover-scale:hover {{
            transform: scale(1.02);
        }}
        
        /* Smooth Scrolling */
        .smooth-scroll {{
            scroll-behavior: smooth;
        }}
        
        /* Reduced Motion */
        @media (prefers-reduced-motion: reduce) {{
            *,
            *::before,
            *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
        </style>
        """
    
    @staticmethod
    def get_chat_styles():
        """Get professional CSS styles for enhanced chat interface"""
        return f"""
        <style>
        /* Professional Chat Container */
        .chat-container {{
            background: linear-gradient(135deg, {StyleManager.COLORS['dark_surface']} 0%, {StyleManager.COLORS['dark_bg']} 100%);
            border-radius: 20px;
            padding: 28px;
            margin: 24px 0;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(16px);
            animation: fadeSlideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* Professional Chat Header */
        .chat-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 2px solid {StyleManager.COLORS['primary']};
            position: relative;
        }}
        
        .chat-header::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 80px;
            height: 2px;
            background: {StyleManager.COLORS['primary_gradient']};
        }}
        
        .chat-title {{
            display: flex;
            align-items: center;
            gap: 16px;
            color: #F8FAFC;
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: -0.01em;
        }}
        
        .chat-avatar {{
            width: 48px;
            height: 48px;
            background: {StyleManager.COLORS['primary_gradient']};
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: white;
            box-shadow: 0 8px 16px -4px rgba(79, 70, 229, 0.4);
        }}
        
        /* Professional Chat Status */
        .chat-status {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 16px;
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.28);
            border-radius: 24px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .chat-status .status-online {{ color: #22c55e; text-shadow: 0 0 6px rgba(34, 197, 94, 0.35); }}
        .chat-status span {{ color: #22c55e; }}
        .status-online {{ color: #22c55e; animation: statusPulse 1.2s ease-in-out infinite; }}
        
        .status-dot {{
            width: 10px;
            height: 10px;
            background: {StyleManager.COLORS['success']};
            border-radius: 50%;
            animation: statusPulse 2s infinite;
        }}
        
        @keyframes statusPulse {{
            0%, 100% {{ 
                opacity: 1; 
                transform: scale(1);
            }}
            50% {{ 
                opacity: 0.6; 
                transform: scale(1.1);
            }}
        }}
        
        /* Professional Message Bubbles */
        .message-container {{
            margin: 20px 0;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        
        .message-user {{
            align-self: flex-end;
            max-width: 75%;
        }}
        
        .message-assistant {{
            align-self: flex-start;
            max-width: 85%;
        }}
        
        .message-bubble {{
            padding: 16px 20px;
            border-radius: 20px;
            position: relative;
            word-wrap: break-word;
            line-height: 1.5;
            font-size: 0.875rem;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .message-bubble.user {{
            background: {StyleManager.COLORS['primary_gradient']};
            color: white;
            border-bottom-right-radius: 8px;
            box-shadow: 0 4px 12px -2px rgba(79, 70, 229, 0.25);
        }}
        
        .message-bubble.assistant {{
            background: rgba(255, 255, 255, 0.08);
            color: #F1F5F9;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-bottom-left-radius: 8px;
            backdrop-filter: blur(8px);
        }}
        
        .message-bubble:hover {{
            transform: translateY(-1px);
        }}
        
        .message-time {{
            font-size: 0.625rem;
            opacity: 0.6;
            margin-top: 6px;
            text-align: right;
            font-weight: 500;
        }}
        
        .message-assistant .message-time {{
            text-align: left;
        }}
        
        /* Professional Typing Indicator */
        .typing-indicator {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px 20px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            border-bottom-left-radius: 8px;
            max-width: 85%;
            margin: 20px 0;
            backdrop-filter: blur(8px);
        }}
        
        .typing-text {{
            color: {StyleManager.COLORS['gray_300']};
            font-size: 0.875rem;
            font-weight: 500;
        }}
        
        .typing-dots {{
            display: flex;
            gap: 6px;
        }}
        
        .typing-dot {{
            width: 10px;
            height: 10px;
            background: {StyleManager.COLORS['primary']};
            border-radius: 50%;
            animation: typingAnimation 1.4s ease-in-out infinite;
        }}
        
        .typing-dot:nth-child(1) {{ animation-delay: -0.32s; }}
        .typing-dot:nth-child(2) {{ animation-delay: -0.16s; }}
        .typing-dot:nth-child(3) {{ animation-delay: 0s; }}
        
        @keyframes typingAnimation {{
            0%, 60%, 100% {{ 
                transform: translateY(0) scale(0.8); 
                opacity: 0.5; 
            }}
            30% {{ 
                transform: translateY(-8px) scale(1); 
                opacity: 1; 
            }}
        }}
        
        /* Professional Suggested Questions */
        .suggested-questions {{
            margin: 24px 0;
            padding: 20px;
            background: rgba(255, 255, 255, 0.04);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(8px);
        }}
        
        .suggested-questions h4 {{
            color: #F8FAFC;
            margin-bottom: 16px;
            font-size: 0.875rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .suggested-questions h4::before {{
            content: '💡';
            font-size: 1rem;
        }}
        
        .question-chips {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .question-chip {{
            padding: 10px 16px;
            background: rgba(79, 70, 229, 0.15);
            border: 1px solid rgba(79, 70, 229, 0.3);
            border-radius: 24px;
            color: {StyleManager.COLORS['primary_light']};
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .question-chip:hover {{
            background: rgba(79, 70, 229, 0.25);
            border-color: rgba(79, 70, 229, 0.5);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px -2px rgba(79, 70, 229, 0.3);
        }}
        
        /* Professional Chat Controls */
        .chat-controls {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin: 20px 0;
            padding: 16px 20px;
            background: rgba(255, 255, 255, 0.04);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(8px);
        }}
        
        .control-group {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .control-label {{
            color: #F1F5F9;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        /* Enhanced Chat Input */
        .stChatInput > div > div {{
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 16px !important;
            backdrop-filter: blur(8px);
        }}
        
        .stChatInput > div > div:focus-within {{
            border-color: {StyleManager.COLORS['primary']} !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        }}
        
        .stChatInput input {{
            color: #F1F5F9 !important;
            background: transparent !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
        }}
        
        .stChatInput input::placeholder {{
            color: rgba(241, 245, 249, 0.5) !important;
        }}
        
        /* Professional Scrollbar */
        .chat-messages {{
            max-height: 60vh;
            overflow-y: auto;
            padding-right: 8px;
        }}
        
        .chat-messages::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .chat-messages::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }}
        
        .chat-messages::-webkit-scrollbar-thumb {{
            background: {StyleManager.COLORS['primary_gradient']};
            border-radius: 8px;
        }}
        
        .chat-messages::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, {StyleManager.COLORS['primary_light']} 0%, {StyleManager.COLORS['primary_dark']} 100%);
        }}
        
        /* Section dividers */
        .section-divider, .section-divider-lg {{
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            margin: 40px 0;
        }}
        .section-divider-lg {{ height: 2px; opacity: 0.9; }}
        
        /* Sticky chat input */
        .chat-input {{
            position: sticky;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            padding: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            z-index: 10;
        }}
        
        /* Light Theme Adjustments */
        [data-theme="light"] .chat-container {{
            background: linear-gradient(135deg, {StyleManager.COLORS['light_card']} 0%, {StyleManager.COLORS['light_surface']} 100%);
            border-color: {StyleManager.COLORS['light_border']};
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
        }}
        
        [data-theme="light"] .chat-title {{
            color: {StyleManager.COLORS['gray_900']};
        }}
        
        [data-theme="light"] .message-bubble.assistant {{
            background: {StyleManager.COLORS['light_surface']};
            color: {StyleManager.COLORS['gray_700']};
            border-color: {StyleManager.COLORS['light_border']};
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .chat-container {{
                padding: 20px 16px;
                margin: 16px 0;
            }}
            
            .chat-header {{
                flex-direction: column;
                gap: 12px;
                align-items: flex-start;
            }}
            
            .message-user, .message-assistant {{
                max-width: 90%;
            }}
            
            .chat-controls {{
                flex-direction: column;
                gap: 12px;
            }}
        }}
        </style>
        """
