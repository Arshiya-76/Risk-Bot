# 📝 Legal Contract Analysis & Risk Assessment Bot

A **GenAI-powered legal assistant** designed for **SMEs** to understand complex contracts, assess risks, and get actionable advice in plain language. Analyze employment, vendor, lease, partnership, and service contracts with clause-by-clause explanations and compliance checks.  

---

## 🚀 Features
- **Risk Scoring:** Identify high-risk clauses.  
- **Clause Explanation:** Simplified business language summaries.  
- **Alternative Suggestions:** Safer or more favorable clause recommendations.  
- **Compliance Check:** Indian law regulations enforcement.  
- **Multi-format Support:** PDF, DOC, and TXT uploads.  
- **Multilingual:** English & Hindi contracts supported.  
- **Audit Trail:** Track all analyses securely.  
- **Reports & Templates:** Generate standardized summaries for legal review.  

---

## 🛠️ Tech Stack
- **Backend & NLP:** Python, spaCy, NLTK  
- **GenAI Analysis:** GPT-4 or Claude 3  
- **Frontend / UI:** Streamlit or Gradio  
- **Other Tools:** pandas, NumPy, file processing libraries  

---

## 📂 Project Structure
```
Risk-Bot/
│
├── app.py                     # Entry point / main script for running the bot
│
├── backend/                   # Core logic for AI, NLP, and risk analysis
│   ├── __init__.py
│   ├── ai_analysis.py          # Functions to call GPT-4 / Claude-3 for legal text analysis
│   ├── nlp_utils.py            # Preprocessing: tokenization, stopwords, lemmatization
│   ├── risk_scoring.py         # Risk scoring functions and models
│   ├── compliance.py           # Compliance checking with Indian legal standards
│   └── report_generator.py     # Functions to create summaries & export results
│
├── frontend/                   # UI components (planned: Streamlit / Gradio)
│   ├── __init__.py
│   ├── ui_components.py        # Custom UI elements for displaying results
│   └── file_upload.py          # File upload handling (PDF, DOC, TXT)
│
├── tests/                      # Unit & integration tests
│   ├── test_ai_analysis.py
│   ├── test_nlp_utils.py
│   ├── test_risk_scoring.py
│   └── test_compliance.py
│
├── data/                       # Sample contracts for testing
│   ├── sample_contract_1.pdf
│   ├── sample_contract_2.docx
│   └── sample_contract_3.txt
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Ignore virtual env, cache files, etc.
└── LICENSE                     # MIT License
```
---
## 🧩 Usage

1. Upload a contract (PDF, DOC, or TXT).  
2. Wait for preprocessing (≤ 2 minutes).  
3. View results:  
   - Risk score (Low, Medium, High)  
   - Highlighted risky clauses  
   - Simplified explanations  
   - Suggested alternatives  
   - Compliance notes  
   - Exportable report  

## 📊 Example Workflow

**Input:** Employment contract  

**Detected Issues:**  
- Unfavorable termination clause  
- Missing non-disclosure clause  
- Potential compliance gaps with Indian labor law  

**Output:**  
- Risk Score: `7.2 / 10` (High Risk)  
- Suggestions: Add fair notice period, insert NDA, revise penalty clause  

## ⚡ Setup & Run
## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
bash
git clone https://github.com/Arshiya-76/Risk-Bot.git
cd Risk-Bot

2️⃣Create Virtual Environment (Recommended)
---

python -m venv venv

 Activate the environment
 
venv\Scripts\activate     # Windows

source venv/bin/activate  # Mac/Linux

3️⃣ Install Dependencies
-
pip install -r requirements.txt

4️⃣ Set Environment Variables
-
Create a .env file and add your API keys (for Claude 3 / GPT-4). Example:

OPENAI_API_KEY=your_api_key_here

ANTHROPIC_API_KEY=your_api_key_here

▶️ Running the Bot
-
.Using Streamlit UI

streamlit run app.py

.Using Gradio UI

python app.py

📦 Requirements
-
spacy

nltk

PyPDF2

python-docx

streamlit

gradio

openai

anthropic

python-dotenv

🤝 Contributing
-
Contributions are welcome!

Fork the repo

Create a branch: git checkout -b feature-new

Commit: git commit -m "Added new feature"

Push: git push origin feature-new

Submit a Pull Request

⚠️ Disclaimer

For educational & demonstration purposes only. Does not constitute legal advice. Use at your own discretion.

## 👥 Project Team

- **Tasleem**  
- **Amal** 


