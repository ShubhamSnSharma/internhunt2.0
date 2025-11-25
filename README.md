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

### 🎯 **Smart Resume Analysis**
- 📄 **Multi-format Support** - Upload PDF or DOCX resumes
- 🤖 **ML Classification** - Automatic role categorization using scikit-learn
- 📊 **Skill Extraction** - NLP-powered skill identification
- 💡 **Career Insights** - Get personalized recommendations

### 🤝 **AI Career Assistant**
- 💬 **Conversational AI** - Powered by Google Gemini
- 🎓 **Career Guidance** - Expert advice on internships and career paths
- 📚 **Context-Aware** - Remembers your resume and preferences
- ⚡ **Real-time Responses** - Fast and accurate answers

### 🔍 **Intelligent Job Matching**
- 🌐 **Multi-source Scraping** - Internshala, LinkedIn, and more
- 🎯 **Personalized Results** - Based on your skills and interests
- 📍 **Location-based** - Filter by city and remote options
- 🔄 **Real-time Updates** - Fresh opportunities daily

### 📚 **Course Recommendations**
- 🎓 **Skill-based Suggestions** - Courses aligned with your career goals
- 🏆 **Top Platforms** - Coursera, Udemy, edX, and more
- 📈 **Learning Paths** - Structured roadmaps for skill development
- ⭐ **Quality Curated** - Only the best courses recommended

### 🎨 **Modern UI/UX**
- 🌙 **Dark Theme** - Easy on the eyes
- ✨ **Glassmorphism** - Modern design aesthetics
- 📱 **Responsive** - Works on all devices
- 🎭 **Smooth Animations** - Delightful user experience

### 🔐 **Admin Dashboard**
- 👨‍💼 **User Management** - Track and manage users
- 📊 **Analytics** - View platform statistics
- 💾 **Cloud Database** - Powered by Neon (PostgreSQL)
- 🌐 **Web-based** - Access from anywhere
- 🔄 **Real-time Sync** - Instant data updates

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
├── 📄 App.py                      # Main application entry point
├── 🎨 styles.py                   # UI styling and themes
├── 🤖 chat_service.py             # Gemini AI chatbot logic
├── 📝 resume_parser.py            # Resume parsing & analysis
├── ⚙️ config.py                   # Configuration management
├── 🛠️ utils.py                    # Utility functions
├── 💾 database.py                 # Database operations
├── 🌐 api_services.py             # External API integrations
├── 🔍 job_scrapers.py             # Job scraping modules
├── ⚠️ error_handler.py            # Error handling
├── 📚 Courses.py                  # Course recommendation logic
├── 🤖 resume_classifier_v2.pkl    # Trained ML model
├── 📊 UpdatedResumeDataSet.csv    # Training dataset
├── 📋 requirements.txt            # Python dependencies
├── 📖 README.md                   # This file
├── 🔐 .env.example                # Environment variables template
├── 🚫 .gitignore                  # Git ignore rules
├── 📁 .streamlit/                 # Streamlit configuration
│   ├── config.toml
│   └── secrets.toml.example
├── 🔤 nevera_font/                # Custom fonts
├── 📂 Uploaded_Resumes/           # User uploaded resumes
└── 📄 pages/                      # Additional Streamlit pages
```

---

## 🤖 Machine Learning Model

### Resume Classification Model

InternHunt uses a **custom-trained ML model** to automatically categorize resumes into job roles.

#### **Model Details:**
- **Algorithm:** scikit-learn classifier (trained on resume dataset)
- **File:** `resume_classifier_v2.pkl` (1.2 MB)
- **Training Data:** `UpdatedResumeDataSet.csv` (3 MB, multiple resume samples)
- **Purpose:** Automatic role categorization from resume text

#### **How It Works:**
1. **Resume Upload** → User uploads PDF/DOCX resume
2. **Text Extraction** → PyPDF2/python-docx extracts text content
3. **NLP Processing** → NLTK tokenizes and cleans the text
4. **Feature Extraction** → Converts text to numerical features
5. **Classification** → ML model predicts the best-fit job role
6. **Results** → Returns role category with confidence score

#### **Supported Job Categories:**
The model can classify resumes into various tech roles including:
- Software Development
- Data Science
- Web Development
- Mobile Development
- DevOps
- And more...

#### **Model Performance:**
- Trained on diverse resume samples
- Uses NLP techniques for text preprocessing
- Optimized for accuracy and speed

#### **Technologies Used:**
- **scikit-learn** - ML framework
- **NLTK** - Text preprocessing
- **Pandas** - Data handling
- **NumPy** - Numerical operations
- **joblib** - Model serialization

---

## 🎯 Usage Guide


### 1️⃣ **Upload Your Resume**
- Click on the file uploader
- Select your PDF or DOCX resume
- Wait for automatic analysis

### 2️⃣ **Explore Recommendations**
- View your classified role
- Check extracted skills
- Browse personalized job matches

### 3️⃣ **Chat with AI Assistant**
- Ask career-related questions
- Get interview tips
- Receive personalized advice

### 4️⃣ **Discover Courses**
- Browse recommended courses
- Filter by platform and topic
- Start learning!

### 5️⃣ **Search for Internships**
- Use filters (location, role, etc.)
- View detailed job descriptions
- Apply directly through links

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
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

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
