<div align="center">

# 🎯 InternHunt

### AI-Powered Internship Matching Platform

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

[![Vercel](https://img.shields.io/badge/Landing-Live_on_Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://internhuntt.vercel.app)
[![Streamlit Cloud](https://img.shields.io/badge/App-Live_on_Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://internhunt.streamlit.app)

**Intelligent Internship Matching Using ML, APIs & Web Data**

---

### 🌐 **Live Demo**

<div align="center">

[![Landing Page](https://img.shields.io/badge/🌟_Landing_Page-Visit_Now-6366F1?style=for-the-badge&labelColor=1e293b)](https://internhuntt.vercel.app)
[![Web App](https://img.shields.io/badge/🚀_Web_App-Try_Live-FF4B4B?style=for-the-badge&labelColor=1e293b)](https://internhunt.streamlit.app)

**👉 Start at the [Landing Page](https://internhuntt.vercel.app) → Click "Upload Resume" → Experience the [Full App](https://internhunt.streamlit.app)!**

</div>

---

[Features](#-features) • [Screenshots](#-screenshots) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack) • [Contributing](#-contributing)

</div>

---

## 📸 Screenshots

> **💡 Want to see it in action? Check out the [Live Demo](https://internhuntt.vercel.app)!**

### 🏠 Landing Page (Vercel)
![Landing Page](./screenshots/landing-page.png)
*Beautiful Figma-designed landing page hosted on Vercel*

### 💼 Resume Analysis
![Resume Upload](./screenshots/resume-upload.png)
*Smart resume parsing and classification*

### 🤖 AI Career Assistant
![AI Chatbot](./screenshots/chatbot.png)
*Powered by Google Gemini for personalized career guidance*

### 🎓 Course Recommendations
![Course Recommendations](./screenshots/courses.png)
*Tailored learning paths based on your profile*

### 🔍 Job Search
![Job Search](./screenshots/job-search.png)
*Real-time internship opportunities from multiple sources*

### 🔐 Admin Dashboard
![Admin Dashboard](./screenshots/admin-dashboard.png)
*User management and analytics powered by Neon PostgreSQL*

---

## ✨ Features

### 📋 **Complete Resume Analysis Pipeline**

#### **1. Resume Upload**
- 📄 **Multi-format Support** - Upload PDF or DOCX resumes
- 🎯 **Drag & Drop Interface** - Easy file upload (50MB limit)
- ✅ **Instant Validation** - Real-time upload status
- 📊 **Basic Info Extraction** - Name, email, phone, LinkedIn

#### **2. Skills Extracted**
- 🔍 **NLP-Powered Detection** - Identifies 100+ technical skills
- 🏷️ **Smart Categorization** - Groups skills by domain
- 📈 **Skill Proficiency** - Detects skill levels from context
- 🎨 **Visual Display** - Clean, organized skill badges

#### **3. AI-Detected Profile**
- 🤖 **ML Classification** - 99.5% accurate role prediction using Logistic Regression
- 🎯 **Top 3 Predictions** - Shows alternative roles with confidence scores
- 📊 **Probability Analysis** - Displays prediction confidence
- 🔄 **25 Job Categories** - From Software Development to Engineering

#### **4. ATS Performance Dashboard**
- 📈 **ATS Score** - Resume compatibility with Applicant Tracking Systems
- 🎯 **Keyword Analysis** - Identifies missing industry keywords
- 📊 **Section Completeness** - Tracks resume sections (3/5, etc.)
- 💡 **Optimization Tips** - Actionable suggestions to improve ATS score

#### **5. Resume Analysis**
- 📝 **Skills Count** - Total technical skills detected (e.g., 19 skills)
- 📄 **Sections Count** - Resume structure analysis (e.g., 3/5 sections)
- 📊 **Completeness Score** - Overall resume quality metric
- 🎯 **Visual Progress** - Clean progress bars and metrics

#### **6. Top Suggestions**
- 💡 **AI-Powered Recommendations** - Personalized resume improvement tips
- ✍️ **Template Suggestions** - Pre-built templates for missing sections
- 🎯 **Priority Ranking** - Numbered suggestions by importance
- 📝 **Quick Actions** - One-click template insertion

**Example Suggestions:**
1. Add detailed work experience with achievements
2. Consider adding a professional summary
3. Add a Work Experience section with achievements and dates
4. Add a short Summary/Objective tailored to the target role

#### **7. Role Alignment Analysis**
- 🎯 **Target Role Matching** - Compares resume against specific job roles
- 📊 **Alignment Score** - Percentage match with target position
- 🔍 **Gap Analysis** - Identifies missing skills/experience
- 💡 **Improvement Roadmap** - Steps to better align with role

#### **8. Job Recommendations**
- 🌐 **Multi-Source Aggregation** - Jobs from Jooble + Internshala
- 🎯 **Personalized Matching** - Based on detected skills and role
- 📍 **Location-based** - Filter by city and remote options
- 🔄 **Real-time Updates** - Fresh opportunities daily
- 📊 **Detailed Listings** - Company, location, salary, requirements

**Sources:**
- **Jooble API** - Global internship opportunities
- **Internshala Scraper** - India-focused internships

#### **9. Recommended Courses**
- 🎓 **Skill-based Suggestions** - Courses aligned with career goals
- 🏆 **Top Platforms** - Coursera, Udemy, edX, and more
- 📈 **Learning Paths** - Structured roadmaps for skill development
- ⭐ **Quality Curated** - Only the best courses recommended
- 🎯 **Role-specific** - Tailored to your detected profile

#### **10. InternHunt Assistant (AI Chatbot)**
- 💬 **Conversational AI** - Powered by Google Gemini
- 🎓 **Career Guidance** - Expert advice on internships and career paths
- 📚 **Context-Aware** - Remembers your resume and preferences
- ⚡ **Real-time Responses** - Fast and accurate answers
- 🤝 **Interview Prep** - Tips, common questions, best practices

---

### 🔐 **Admin Dashboard**
- 👨‍💼 **User Management** - Track all uploaded resumes
- 📊 **Analytics** - View platform statistics and insights
- 💾 **Cloud Database** - Powered by Neon PostgreSQL
- 🌐 **Web-based** - Access from anywhere
- 🔄 **Real-time Sync** - Instant data updates
- 📈 **Resume Database** - All uploaded resumes stored securely

---

### 🎨 **Modern UI/UX**
- 🌙 **Dark Theme** - Easy on the eyes
- ✨ **Glassmorphism** - Modern design aesthetics
- 📱 **Responsive** - Works on all devices
- 🎭 **Smooth Animations** - Delightful user experience
- 🎯 **Intuitive Flow** - Seamless user journey from upload to job search

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ShubhamSnSharma/internhunt2.git
cd internhunt2
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data** (Required for NLP)
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

5. **Set up environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
# GEMINI_API_KEY=your_api_key_here
# GEMINI_MODEL=gemini-1.5-flash
```

6. **Run the application**
```bash
streamlit run App.py
```

The app will open in your browser at `http://localhost:8501` 🎉

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Neon Database (PostgreSQL) - Production
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# MySQL (Local Development - Optional)
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=internhunt
```

### Streamlit Secrets (For Deployment)

For Streamlit Cloud deployment, add secrets in the dashboard:

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your_api_key_here"
GEMINI_MODEL = "gemini-1.5-flash"

# Neon Database
DATABASE_URL = "postgresql://user:password@host.neon.tech/dbname?sslmode=require"
```

### Setting up Neon Database

1. **Create a Neon account** at [neon.tech](https://neon.tech)
2. **Create a new project** and database
3. **Copy the connection string** from the dashboard
4. **Add to `.env`** file as `DATABASE_URL`
5. **Run migrations** (if any) to set up tables

---

## � Deployment Architecture

This project uses a **dual-deployment strategy** for optimal user experience:

### 🎨 **Landing Page** (Vercel)
- **URL:** [internhuntt.vercel.app](https://internhuntt.vercel.app)
- **Tech:** React + TypeScript + Tailwind CSS v4
- **Design:** Figma → React components
- **Features:** Glassmorphism, smooth animations (Motion)
- **Icons:** Lucide React
- **UI Components:** Shadcn/ui
- **Hosting:** Vercel (Fast CDN, global edge network)

### ⚡ **Web Application** (Streamlit Cloud)
- **URL:** [internhunt.streamlit.app](https://internhunt.streamlit.app)
- **Tech:** Python + Streamlit
- **Purpose:** Full-featured AI-powered platform
- **Hosting:** Streamlit Cloud (Free Python app hosting)

### � **Database** (Neon)
- **Service:** [Neon](https://neon.tech) - Serverless PostgreSQL
- **Purpose:** User data, analytics, admin dashboard
- **Migration:** Originally MySQL (local) → Now Neon (cloud)
- **Benefits:** Auto-scaling, branching, serverless

### �🔗 **How They Connect**
```
User visits Landing Page (Vercel)
         ↓
Clicks "Upload Resume" button
         ↓
Redirects to Web App (Streamlit)
         ↓
App connects to Neon Database
         ↓
Full InternHunt experience!
```

### 📦 **Deploy Your Own**

#### **Vercel (Landing Page)**
1. Push your landing page code to GitHub
2. Import project on [Vercel](https://vercel.com)
3. Deploy with one click!

#### **Streamlit Cloud (Web App)**
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add secrets (API keys) in dashboard
5. Deploy!

#### **Neon (Database)**
1. Create account at [neon.tech](https://neon.tech)
2. Create a new PostgreSQL database
3. Copy connection string
4. Add to Streamlit secrets as `DATABASE_URL`
5. Database is ready!

---
## 🛠️ Tech Stack

### **Landing Page (Vercel)**
- ![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB) **React** - UI library
- ![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=white) **TypeScript** - Type-safe JavaScript
- ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white) **Tailwind CSS v4** - Utility-first CSS
- ![Motion](https://img.shields.io/badge/Motion-FF0080?style=flat-square&logo=framer&logoColor=white) **Motion** - Animation library
- **Shadcn/ui** - Component library
- **Lucide React** - Icon library

### **Web Application (Streamlit)**
- ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) **Streamlit** - Web framework
- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) **HTML/CSS** - Custom styling
- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) **JavaScript** - Interactive elements

### **Backend & ML**
- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) **Python 3.9+** - Core language
- ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white) **scikit-learn** - ML classification
- ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white) **PyTorch** - Deep learning
- ![NLTK](https://img.shields.io/badge/NLTK-154f3c?style=flat-square) **NLTK** - Natural language processing

### **AI & APIs**
- ![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=flat-square&logo=google&logoColor=white) **Google Gemini** - Conversational AI
- ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-43B02A?style=flat-square) **BeautifulSoup** - Web scraping
- ![Requests](https://img.shields.io/badge/Requests-2CA5E0?style=flat-square) **Requests** - HTTP library

### **Data Processing**
- ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) **Pandas** - Data manipulation
- ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white) **NumPy** - Numerical computing
- **PyPDF2 & python-docx** - Document parsing

### **Database**
- ![Neon](https://img.shields.io/badge/Neon-00E599?style=flat-square&logo=postgresql&logoColor=white) **Neon** - Serverless PostgreSQL
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white) **PostgreSQL** - Relational database
- ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white) **MySQL** - Alternative database (local development)

---

## 📁 Project Structure

```
internhunt2/
├── 📄 App.py                           # Main Streamlit application entry point
├── 🎨 styles.py                        # Centralized UI styling and themes
├── 🤖 chat_service.py                  # Gemini AI chatbot service
├── 📝 resume_parser.py                 # Resume parsing & NLP analysis
├── ⚙️ config.py                        # Configuration management
├── 🛠️ utils.py                         # Utility functions
├── 💾 database.py                      # Neon PostgreSQL database operations
├── 🌐 api_services.py                  # External API integrations (Jooble)
├── 🔍 job_scrapers.py                  # Job scraping (Internshala)
├── ⚠️ error_handler.py                 # Error handling & logging
├── 📚 Courses.py                       # Course recommendation engine
│
├── 🤖 resume_classifier_v2.pkl         # Trained ML model (1.2 MB)
├── 📊 UpdatedResumeDataSet.csv         # Training dataset (962 samples)
├── 📓 ResumeClassification_Model.ipynb # Model training notebook
│
├── 📋 requirements.txt                 # Python dependencies
├── 📖 README.md                        # Project documentation
├── 📜 LICENSE                          # MIT License
├── 🔒 PRIVACY.md                       # Privacy policy
├── 🔐 .env.example                     # Environment variables template
├── 🚫 .gitignore                       # Git ignore rules
│
├── 📁 .streamlit/                      # Streamlit configuration
│   ├── config.toml                     # App configuration
│   └── secrets.toml.example            # Secrets template
│
├── 🔤 nevera_font/                     # Custom Nevera font files
│   ├── Nevera-Bold.ttf
│   ├── Nevera-Regular.ttf
│   └── Nevera-Light.ttf
│
├── 📂 Uploaded_Resumes/                # User uploaded resume storage
│   └── .gitkeep                        # Preserve directory in Git
│
├── � screenshots/                     # Application screenshots for README
│   ├── landing-page.png                # Vercel landing page
│   ├── resume-upload.png               # Resume upload interface
│   ├── skills-extracted.png            # Skills detection display
│   ├── ai-profile.png                  # ML role prediction
│   ├── ats-dashboard.png               # ATS performance metrics
│   ├── suggestions.png                 # AI improvement suggestions
│   ├── chatbot.png                     # Gemini AI assistant
│   ├── courses.png                     # Course recommendations
│   ├── job-search.png                  # Job listings
│   └── admin-dashboard.png             # Admin panel
│
└── 🐍 venv/                            # Virtual environment (not in Git)
```

### **Key Files Explained:**

**Core Application:**
- `App.py` - Main Streamlit app with complete user flow (3814 lines)
- `styles.py` - All CSS styling, glassmorphism, animations (70KB)
- `chat_service.py` - Google Gemini integration for AI chatbot

**Data Processing:**
- `resume_parser.py` - spaCy-based NLP for skill extraction
- `utils.py` - Helper functions for text processing
- `database.py` - Neon PostgreSQL connection and queries

**External Integrations:**
- `api_services.py` - Jooble API for global job listings
- `job_scrapers.py` - Internshala web scraping
- `Courses.py` - Course recommendation logic

**ML Model:**
- `resume_classifier_v2.pkl` - Logistic Regression + TF-IDF (99.5% accuracy)
- `UpdatedResumeDataSet.csv` - 962 resume samples, 25 categories
- `ResumeClassification_Model.ipynb` - Training notebook (Google Colab)

**Configuration:**
- `.env.example` - Template for API keys (Gemini, Database)
- `.streamlit/config.toml` - Streamlit theme and settings
- `requirements.txt` - 30+ Python packages

**Documentation:**
- `README.md` - Complete project documentation
- `LICENSE` - MIT License
- `PRIVACY.md` - Privacy policy for users

---

## 🤖 Machine Learning Model

### Resume Classification Model

InternHunt uses a **custom-trained Logistic Regression model** with TF-IDF vectorization to automatically categorize resumes into 25 job roles with **99.5% accuracy**.

#### **Model Architecture:**
- **Algorithm:** Logistic Regression (scikit-learn 1.7.2)
- **Vectorization:** TF-IDF (Term Frequency-Inverse Document Frequency)
- **Pipeline:** TfidfVectorizer → LogisticRegression
- **File:** `resume_classifier_v2.pkl` (1.2 MB)
- **Training Data:** `UpdatedResumeDataSet.csv` (962 resume samples)

#### **Model Performance:**
| Metric | Score |
|--------|-------|
| **Test Accuracy** | **99.48%** |
| **Precision** | **99.6%** (weighted) |
| **Recall** | **99.5%** (weighted) |
| **F1-Score** | **99.5%** (weighted) |
| **Cross-Validation** | **99.48% ± 0.97%** (5-fold) |

#### **Training Configuration:**
```python
Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=5000,        # Limit features to prevent overfitting
        ngram_range=(1, 2),       # Use unigrams and bigrams
        min_df=2,                 # Ignore terms in < 2 documents
        max_df=0.95,              # Ignore terms in > 95% of documents
        stop_words='english',     # Remove common English stop words
        lowercase=True            # Normalize case
    )),
    ('classifier', LogisticRegression(
        max_iter=1000,
        class_weight='balanced',  # Handle class imbalance
        random_state=42,
        C=1.0                     # Regularization strength
    ))
])
```

#### **Dataset Split:**
- **Training Set:** 769 samples (80%)
- **Test Set:** 193 samples (20%)
- **Stratified Split:** Maintains class distribution
- **Total Classes:** 25 job categories

#### **How It Works:**
1. **Resume Upload** → User uploads PDF/DOCX resume
2. **Text Extraction** → PyPDF2/python-docx extracts raw text
3. **Text Cleaning** → Remove HTML tags, URLs, extra whitespace
4. **TF-IDF Vectorization** → Convert text to numerical features (5000 features max)
5. **Classification** → Logistic Regression predicts job category
6. **Probability Analysis** → Returns confidence scores for top 3 predictions

#### **Supported Job Categories (25 Total):**

**Programming & Development:**
- Java Developer (84 samples)
- Python Developer (48 samples)
- DotNet Developer (28 samples)
- Web Designing (45 samples)
- SAP Developer (24 samples)

**Data & AI:**
- Data Science (40 samples)
- Hadoop (42 samples)
- ETL Developer (40 samples)
- Database (33 samples)

**DevOps & Infrastructure:**
- DevOps Engineer (55 samples)
- Network Security Engineer (25 samples)

**Testing:**
- Testing (70 samples)
- Automation Testing (26 samples)

**Engineering:**
- Mechanical Engineer (40 samples)
- Electrical Engineering (30 samples)
- Civil Engineer (24 samples)

**Business & Operations:**
- Business Analyst (28 samples)
- Operations Manager (40 samples)
- PMO (30 samples)
- HR (44 samples)
- Sales (40 samples)

**Specialized:**
- Blockchain (40 samples)
- Advocate (20 samples)
- Arts (36 samples)
- Health and fitness (30 samples)

#### **Model Features:**
- ✅ **Multi-class Classification** - Predicts from 25 categories
- ✅ **Probability Scores** - Returns confidence for each prediction
- ✅ **Top-3 Predictions** - Shows 3 most likely roles with probabilities
- ✅ **Version Compatibility** - Warns if sklearn version mismatch
- ✅ **Balanced Classes** - Uses class_weight='balanced' for fair predictions
- ✅ **Fallback Handling** - Graceful degradation if model unavailable

#### **Technical Implementation:**
```python
# Model loading with version check
data = joblib.load("resume_classifier_v2.pkl")
model = data["model"]  # Pipeline object
sklearn_version = data.get("sklearn_version")  # "1.7.2"

# Prediction with probabilities
predicted_category = model.predict([resume_text])[0]
probabilities = model.predict_proba([resume_text])[0]
classes = model.classes_

# Top 3 predictions
top_3_idx = probabilities.argsort()[-3:][::-1]
top_3_predictions = [
    {"category": classes[idx], "probability": probabilities[idx]}
    for idx in top_3_idx
]
```

#### **Training Details:**
- **Trained on:** Google Colab
- **Training Time:** < 1 minute
- **Notebook:** `ResumeClassification_Model.ipynb`
- **scikit-learn Version:** 1.7.2
- **Random State:** 42 (for reproducibility)

#### **Technologies Used:**
- **scikit-learn 1.7.2** - ML framework (Logistic Regression, TF-IDF)
- **joblib** - Model serialization and loading
- **pandas** - Data manipulation and preprocessing
- **PyPDF2 / python-docx** - Resume text extraction
- **Streamlit caching** - Fast model loading with `@st.cache_resource`

---

## 🎯 Usage Guide

### **Complete User Journey**

#### **Step 1: Upload Your Resume** 📄
1. Visit [internhunt.streamlit.app](https://internhunt.streamlit.app)
2. Drag and drop your resume or click "Browse files Resume"
3. Supported formats: PDF, DOCX (max 50MB)
4. Wait for upload confirmation ✅

#### **Step 2: View Basic Info** 👤
- **Name** extracted from resume
- **Email** address detected
- **Phone** number identified
- **LinkedIn** profile link (if present)

#### **Step 3: Skills Extracted** 🔍
- View all **technical skills** detected from your resume
- Skills organized by category (Programming, Frameworks, Tools, etc.)
- **19+ skills** typically identified
- Clean visual display with skill badges

#### **Step 4: AI-Detected Profile** 🤖
- See your **predicted job role** (99.5% accuracy)
- View **Top 3 role predictions** with confidence scores
- Example: "Python Developer (85%), Data Scientist (10%), Web Developer (5%)"
- Understand which category best fits your profile

#### **Step 5: ATS Performance Dashboard** 📊
- Check your **ATS compatibility score**
- See **keyword analysis** and missing terms
- View **section completeness** (e.g., 3/5 sections)
- Get optimization tips to improve ATS score

#### **Step 6: Resume Analysis** 📝
- **Skills Count**: Total skills detected (e.g., 19 skills)
- **Sections Count**: Resume structure (e.g., 3/5 sections)
- **Completeness Score**: Overall quality metric
- Visual progress bars for each metric

#### **Step 7: Top Suggestions** 💡
Review AI-powered recommendations:
1. Add detailed work experience with achievements
2. Consider adding a professional summary
3. Add a Work Experience section with achievements and dates
4. Add a short Summary/Objective tailored to the target role

**Quick Actions:**
- ✨ Add Work Experience Template
- 📝 Add Summary/Objective Template

#### **Step 8: Role Alignment Analysis** 🎯
- See how your resume aligns with target roles
- View **alignment percentage** for specific positions
- Identify **skill gaps** and missing experience
- Get roadmap to improve role fit

#### **Step 9: Job Recommendations** 🌐
Browse personalized internship opportunities:

**From Jooble:**
- Global internship listings
- Filtered by your detected role
- Location-based results

**From Internshala:**
- India-focused internships
- Real-time scraping
- Detailed company info, stipend, duration
- Direct application links

#### **Step 10: Recommended Courses** 🎓
- View courses tailored to your profile
- Platforms: Coursera, Udemy, edX, etc.
- Organized by skill development path
- Click to enroll directly

#### **Bonus: InternHunt Assistant** 🤖
- Open sidebar chat
- Ask career questions
- Get interview tips
- Receive personalized advice
- Powered by Google Gemini AI

---

### **Admin Dashboard Access** 🔐
*For administrators only*

1. Access admin panel
2. View all uploaded resumes
3. Check user analytics
4. Monitor platform statistics
5. Manage resume database (Neon PostgreSQL)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions
- Test your changes thoroughly
- Update documentation as needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Shubham Sharma**

- GitHub: [@ShubhamSnSharma](https://github.com/ShubhamSnSharma)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/ShubhamSnSharma)
- Email: shubhamsharma99918@gmail.com

---

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) for the amazing AI capabilities
- [Streamlit](https://streamlit.io/) for the fantastic web framework
- [Internshala](https://internshala.com/) for internship data
- All open-source contributors

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/ShubhamSnSharma/internhunt2?style=social)
![GitHub forks](https://img.shields.io/github/forks/ShubhamSnSharma/internhunt2?style=social)
![GitHub issues](https://img.shields.io/github/issues/ShubhamSnSharma/internhunt2)
![GitHub pull requests](https://img.shields.io/github/issues-pr/ShubhamSnSharma/internhunt2)

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

Made with ❤️ by Shubham Sharma

</div>
