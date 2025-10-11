# 🗂️ AIATL Project Structure

This document describes the reorganized file structure of the AIATL (AI-Assisted Triage and Learning System) project.

## 📁 Directory Structure

```
AIATL_Project-1/
├── README.md                    # Main project documentation
├── STRUCTURE.md                 # This file - structure documentation
├── requirements.txt             # Python dependencies
├── main.py                     # Application entry point
├── 
├── app/                        # Main Streamlit application
│   ├── __init__.py
│   ├── main.py                 # App configuration and routing
│   ├── pages/                  # Streamlit pages
│   │   ├── __init__.py
│   │   ├── home.py             # Home page
│   │   ├── login.py            # User authentication
│   │   ├── register.py          # User registration
│   │   ├── patient_dashboard.py # Patient interface
│   │   └── doctor_dashboard.py # Doctor interface
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── helpers.py           # Helper functions
│   │   └── database.py          # Database operations
│   └── static/                 # Static assets
│       ├── css/
│       │   └── styles.css
│       └── images/
│           └── logo.png
│
├── ai_crew/                   # AI CrewAI system
│   ├── __init__.py
│   ├── config/                # Configuration files
│   │   ├── agents.yaml        # Agent definitions
│   │   └── tasks.yaml         # Task definitions
│   ├── agents/                # Agent implementations
│   │   ├── __init__.py
│   │   └── crew.py            # Crew orchestration
│   ├── tools/                 # Custom AI tools
│   │   ├── __init__.py
│   │   └── medical_rag.py     # RAG tools for medical knowledge
│   └── main.py                # Crew execution entry point
│
├── data/                      # Data and reports
│   ├── medical_reports/       # Medical knowledge bases
│   │   ├── cardiologist_report.txt
│   │   ├── neurologist_report.txt
│   │   └── pulmonologist_report.txt
│   ├── analysis_outputs/      # AI analysis results
│   │   ├── cardiologist_analysis.txt
│   │   ├── neurologist_analysis.txt
│   │   ├── pulmonologist_analysis.txt
│   │   └── final_report.txt
│   └── sample_data/           # Sample data files
│       └── sample_report.pdf
│
├── models/                    # Data models
│   ├── __init__.py
│   ├── user.py               # User data model
│   └── doctor.py             # Doctor data model
│
├── services/                 # Business logic services
│   ├── __init__.py
│   ├── email_service.py      # Email functionality
│   └── database_service.py   # Database operations
│
└── tests/                    # Test files
    ├── __init__.py
    ├── test_models.py
    └── test_services.py
```

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file with your API keys:
```bash
GOOGLE_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
MONGODB_URI=your_mongodb_connection_string
```

### 3. Run the Application
```bash
streamlit run main.py
```

## 📋 Key Improvements

### ✅ **Organized Structure**
- **Clear separation** of concerns (app, AI crew, data, models, services)
- **Meaningful names** for all files and directories
- **Logical grouping** of related functionality

### ✅ **Better Maintainability**
- **Modular design** with proper Python packages
- **Consistent naming** conventions
- **Clear import paths** throughout the codebase

### ✅ **Scalability**
- **Easy to extend** with new features
- **Test-ready** structure with dedicated test directory
- **Service-oriented** architecture for business logic

### ✅ **Developer Experience**
- **Intuitive navigation** through the codebase
- **Clear documentation** of structure and purpose
- **Standard Python project** layout

## 🔧 Migration Notes

### File Path Changes
- All imports have been updated to use the new structure
- Static assets moved to `app/static/`
- AI crew files moved to `ai_crew/`
- Data files organized in `data/` directory

### Import Updates
- `from utils.helpers` → `from app.utils.helpers`
- `from aiatl1.src.crew_methods.main` → `from ai_crew.main`
- All file paths updated to reflect new structure

This reorganization makes the project much more maintainable, scalable, and follows Python best practices! 🎉
