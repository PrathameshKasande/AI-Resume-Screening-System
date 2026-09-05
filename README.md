# 🤖 AI Resume Screening System

An **NLP and Machine Learning based Resume Screening System** that automatically compares a candidate's resume with a manually provided Job Description (JD), calculates a resume-job match score, identifies matched and missing skills, and provides an easy-to-understand screening result through an interactive Streamlit dashboard.

The project combines **Semantic Similarity, TF-IDF Similarity, and Skill Matching** to automate the initial resume screening process.


## 📌 Problem Statement

Recruiters spend significant time manually comparing resumes with job descriptions to identify suitable candidates.

This project solves this problem by automatically analyzing a resume against a JD, calculating a match score, identifying matched and missing skills, and reducing manual resume screening effort.


## 🎯 Project Objective

The main objective is to build an **AI-assisted resume screening system** that can:

* Extract text from resume PDF files.
* Accept Job Descriptions through manual copy-paste.
* Clean and preprocess resume and JD text.
* Extract relevant technical skills.
* Compare resume content with job requirements.
* Calculate resume-JD similarity.
* Identify matched skills.
* Identify missing skills.
* Generate an overall candidate match score.
* Provide an understandable screening explanation.
* Display results through an interactive dashboard.
* Evaluate the matching system using standard ML classification metrics.
* Support Docker-based deployment.

# ⭐ Key Features

### 📄 Resume Upload

Users can upload a resume in PDF format directly from their local device.

### 📝 Manual Job Description Input

Users can copy and paste a Job Description directly into the application instead of uploading a JD file.

### 🧹 NLP Text Preprocessing

The system performs basic text cleaning including:

* Lowercase conversion
* Special-character handling
* Whitespace normalization

The preprocessing pipeline converts text into a normalized form before matching.

### 🔍 Skill Extraction

The system extracts skills from both the resume and Job Description and compares them to determine skill coverage.

The skill matching calculation measures the percentage of JD-required skills found in the candidate resume.

### 🧠 Semantic Similarity

The system uses the **Sentence Transformers `all-MiniLM-L6-v2` model** to generate sentence embeddings and calculate semantic similarity between the resume and JD.

### 📊 TF-IDF Similarity

TF-IDF vectors are compared using cosine similarity to measure textual similarity between the resume and Job Description.

### 🎯 Hybrid Resume Matching

The final score combines three signals:

```text
Semantic Similarity
        +
Skill Match
        +
TF-IDF Similarity
        ↓
Final Resume-JD Match Score
```

Current scoring weights:

```text
Semantic Similarity → 45%
Skill Match         → 35%
TF-IDF Similarity   → 20%
```

These weights are implemented in the scoring module.

### 📉 Skill Gap Analysis

The system helps identify:

```text
Matched Skills
       +
Missing Skills
       ↓
Skill Gap
```

This allows a candidate or recruiter to understand which required skills are present and which are missing.

### 💡 Explainable Screening Result

The application provides an explanation of the candidate's screening result rather than displaying only a numerical score.

### 📈 Interactive Dashboard

The Streamlit interface presents:

* Resume analysis
* Job Description analysis
* Match score
* Similarity scores
* Matched skills
* Missing skills
* Screening recommendation
* Skill gap information


# 🏗️ System Architecture

```text
                     USER
                       │
                       ▼
            ┌────────────────────┐
            │   Streamlit UI     │
            └─────────┬──────────┘
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
       Resume PDF          Manual JD
             │                 │
             ▼                 ▼
      Resume Parser        JD Parser
             │                 │
             └────────┬────────┘
                      ▼
             Text Preprocessing
                      │
                      ▼
               Skill Extraction
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
       TF-IDF Similarity   Semantic Similarity
             │                 │
             └────────┬────────┘
                      │
                      ▼
                 Skill Matching
                      │
                      ▼
              Hybrid Score Engine
                      │
                      ▼
              Final Match Score
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
         Skill Gap         Explanation
             │                 │
             └────────┬────────┘
                      ▼
               Dashboard Result
```

---

# 🔄 End-to-End Workflow

```text
Upload Resume PDF
        ↓
Extract Resume Text
        ↓
Clean Resume Text
        ↓
Paste Job Description
        ↓
Process Job Description
        ↓
Extract Resume Skills
        ↓
Extract JD Skills
        ↓
Calculate TF-IDF Similarity
        ↓
Calculate Semantic Similarity
        ↓
Calculate Skill Match
        ↓
Calculate Hybrid Match Score
        ↓
Identify Matched Skills
        ↓
Identify Missing Skills
        ↓
Generate Explanation
        ↓
Display Dashboard
```


# 🧠 NLP / ML Methodology

## 1. Resume Text Extraction

The uploaded PDF is processed to extract the textual content of the candidate's resume.

```text
Resume.pdf
    ↓
PDF Text Extraction
    ↓
Resume Text
```


## 2. Text Preprocessing

The extracted text is normalized before further NLP processing.

The current preprocessing includes:

```text
Raw Text
   ↓
Lowercase
   ↓
Remove/normalize unwanted characters
   ↓
Normalize whitespace
   ↓
Clean Text
```


## 3. Skill Matching

The system extracts skills from:

```text
Candidate Resume
       +
Job Description
       ↓
Skill Comparison
       ↓
Matched Skills
       +
Missing Skills
```

For example:

```text
Resume:
Python
SQL
Pandas
Machine Learning

JD:
Python
SQL
Pandas
Power BI
Machine Learning
```

Output:

```text
Matched Skills:
Python
SQL
Pandas
Machine Learning

Missing Skill:
Power BI
```


## 4. TF-IDF Similarity

TF-IDF is used to convert resume and JD text into numerical representations.

Cosine similarity is then used to calculate textual similarity.

```text
Resume Text
     ↓
TF-IDF Vector
     │
     │ Cosine Similarity
     │
JD Text
     ↓
TF-IDF Vector
```

---

## 5. Semantic Similarity

The project uses:

```text
all-MiniLM-L6-v2
```

to generate sentence embeddings.

```text
Resume
   ↓
Sentence Embedding
   │
   │ Cosine Similarity
   │
JD
   ↓
Sentence Embedding
```

This helps compare the semantic meaning of resume and JD content rather than relying only on exact keyword overlap.



# 🎯 Hybrid Scoring

The project combines three matching signals.

| Component           |   Weight |
| ------------------- | -------: |
| Semantic Similarity |      45% |
| Skill Match         |      35% |
| TF-IDF Similarity   |      20% |
| **Total**           | **100%** |

Formula:

```text
Final Score =
(
    Semantic Score × 0.45
    +
    Skill Score × 0.35
    +
    TF-IDF Score × 0.20
) × 100
```

The resulting score is converted into a percentage from 0 to 100.


# 📊 Model Evaluation

The project includes an evaluation pipeline to measure how well the screening system classifies resume-JD matches.

The evaluation uses standard machine learning metrics:

* Accuracy
* Precision
* Recall
* F1 Score

## Current Evaluation Result

The latest evaluation result for this project is:

| Metric        |       Score |
| ------------- | ----------: |
| **Accuracy**  |  **81.00%** |
| **Precision** | **100.00%** |
| **Recall**    |  **76.25%** |
| **F1 Score**  |  **86.52%** |

### Interpretation

**81% Accuracy** means that 81% of the evaluated resume-JD classification decisions were correct.

**100% Precision** means that the candidates classified as positive matches in this evaluation were all positive according to the benchmark labels.

**76.25% Recall** means the system identified 76.25% of the actual positive matches.

**86.52% F1 Score** represents the balance between precision and recall.

> **Important:** These metrics are benchmark results for the project's current evaluation dataset. They should not be interpreted as real-world hiring accuracy.


# 🎚️ Threshold Optimization

The project also includes a threshold optimization script.

Run:

```cmd
python evaluation\find_best_threshold.py
```

The current evaluation found:

```text
Best Threshold : 50%
Accuracy       : 100.00%
Precision      : 100.00%
Recall         : 100.00%
F1 Score       : 100.00%
```

However, the **model evaluation result reported for the project is 81% Accuracy, 100% Precision, 76.25% Recall, and 86.52% F1 Score** under the evaluation configuration used for the reported result.

The threshold-optimization result should therefore be presented separately from the main model evaluation result.



# 🛠️ Technology Stack

## Programming

* Python

## NLP

* Natural Language Processing
* Text Preprocessing
* Skill Extraction
* TF-IDF
* Sentence Embeddings
* Semantic Similarity
* Cosine Similarity

## Machine Learning

* Scikit-learn
* Classification Metrics
* Feature Engineering
* Threshold Optimization

## Deep Learning / Embeddings

* Sentence Transformers
* `all-MiniLM-L6-v2`

## Data Processing

* Pandas
* NumPy

## PDF Processing

* PyMuPDF

## Frontend

* Streamlit

## Testing

* Pytest

## Deployment / DevOps

* Docker
* Git
* GitHub

## Development Environment

* VS Code
* Windows 11
* Python Virtual Environment



# 📂 Project Structure

```text
AI-Resume-Screening-System/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── Dockerfile
│
├── data/
│   ├── resumes/
│   │   ├── sample_resume_01.pdf
│   │   ├── sample_resume_02.pdf
│   │   └── ...
│   │
│   ├── job_descriptions/
│   │   ├── data_analyst.txt
│   │   ├── data_scientist.txt
│   │   ├── ml_engineer.txt
│   │   └── nlp_engineer.txt
│   │
│   └── evaluation/
│       ├── labeled_matches.csv
│       │
│       ├── synthetic_resumes/
│       │   ├── resume_001.txt
│       │   ├── resume_002.txt
│       │   └── ...
│       │
│       └── results/
│           └── evaluation_results.csv
│
├── src/
│   ├── __init__.py
│   ├── resume_parser.py
│   ├── jd_parser.py
│   ├── text_preprocessor.py
│   ├── skill_extractor.py
│   ├── feature_extractor.py
│   ├── similarity.py
│   ├── scoring.py
│   ├── ranking.py
│   ├── skill_gap.py
│   ├── explanation.py
│   └── utils.py
│
├── evaluation/
│   ├── evaluate_matching.py
│   ├── evaluate_ranking.py
│   ├── find_best_threshold.py
│   └── metrics.py
│
├── scripts/
│   └── generate_evaluation_data.py
│
├── tests/
│   ├── test_parser.py
│   ├── test_similarity.py
│   └── test_scoring.py
│
└── assets/
    └── screenshots/
```



# ⚙️ Installation and Setup

## Prerequisites

Install the following:

* Python 3.x
* Git
* Docker Desktop (optional, for container deployment)
* VS Code (recommended)



# 💻 Run on Windows 11

## Step 1 — Clone the Repository

```cmd
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Move into the project:

```cmd
cd AI-Resume-Screening-System
```



## Step 2 — Create Virtual Environment

```cmd
python -m venv venv
```


## Step 3 — Activate Virtual Environment

For Windows CMD:

```cmd
venv\Scripts\activate
```

You should see:

```text
(venv)
```

before your command prompt.


## Step 4 — Upgrade pip

```cmd
python -m pip install --upgrade pip
```



## Step 5 — Install Dependencies

```cmd
pip install -r requirements.txt
```


# ▶️ Run the Application

Start the Streamlit application:

```cmd
streamlit run app.py
```

The application will open in your browser.

Typical local address:

```text
http://localhost:8501
```



# 🖥️ How to Use the Application

## Step 1

Open the Streamlit application.

## Step 2

Upload a candidate resume:

```text
Resume PDF
```

## Step 3

Copy and paste the required Job Description manually.

Example:

```text
We are looking for a Data Analyst with experience
in Python, SQL, Pandas, Power BI and data visualization.
```

## Step 4

Click:

```text
Analyze Resume
```

## Step 5

Review:

```text
Resume Match Score
        ↓
Matched Skills
        ↓
Missing Skills
        ↓
Similarity Scores
        ↓
Skill Gap
        ↓
Screening Explanation
        ↓
Dashboard
```

---

# 🧪 Evaluation From Scratch

## Generate Evaluation Data

If the evaluation dataset has not been generated:

```cmd
python scripts\generate_evaluation_data.py
```

---

## Run Matching Evaluation

```cmd
python evaluation\evaluate_matching.py
```

The evaluation results are stored in:

```text
data\evaluation\results\evaluation_results.csv
```

---

## Optimize Threshold

```cmd
python evaluation\find_best_threshold.py
```

This tests different classification thresholds and reports:

```text
Accuracy
Precision
Recall
F1 Score
```

---

# 🧪 Run Tests

Run all tests:

```cmd
pytest
```

Run individual tests:

```cmd
pytest tests\test_parser.py
```

```cmd
pytest tests\test_similarity.py
```

```cmd
pytest tests\test_scoring.py
```

---

# 🐳 Docker

The project includes Docker support for reproducible deployment.

## Build Docker Image

From the project root:

```cmd
docker build -t ai-resume-screening .
```

## Run Docker Container

```cmd
docker run -p 8501:8501 ai-resume-screening
```

Then open:

```text
http://localhost:8501
```

---

# 🔀 Git and GitHub

Initialize Git if required:

```cmd
git init
```

Check the repository:

```cmd
git status
```

Add files:

```cmd
git add .
```

Commit:

```cmd
git commit -m "Complete AI Resume Screening System"
```

Add your GitHub repository:

```cmd
git remote add origin <YOUR-GITHUB-REPOSITORY-URL>
```

Push:

```cmd
git branch -M main
git push -u origin main
```

For future updates:

```cmd
git add .
git commit -m "Update resume screening system"
git push
```

---

# 🔐 Data Privacy

Resumes may contain personal information such as:

* Name
* Email
* Phone number
* Address
* Education
* Employment history

For a production deployment:

* Do not expose private resumes publicly.
* Avoid unnecessary resume storage.
* Secure uploaded files.
* Do not commit personal resumes to GitHub.
* Use synthetic/sample resumes for demonstrations.
* Follow applicable privacy and data-protection requirements.

This project should be treated as an **AI-assisted screening tool**, not as an autonomous hiring decision system.

---

# 📸 Screenshots

Add application screenshots to:

```text
assets/screenshots/
```

Recommended screenshots:

```text
01_home.png
02_resume_upload.png
03_jd_input.png
04_analysis_result.png
05_skill_gap.png
06_dashboard.png
```

Example:

```markdown
![Resume Screening Dashboard](assets/screenshots/dashboard.png)
```

---

# 📊 Project Results

### Current Evaluation

```text
Accuracy  : 81.00%
Precision : 100.00%
Recall    : 76.25%
F1 Score  : 86.52%
```

### Matching Strategy

```text
Semantic Similarity → 45%
Skill Matching      → 35%
TF-IDF Similarity   → 20%
```

### Application

```text
Streamlit Web Application
```

### Input

```text
Resume PDF
+
Manual Job Description
```

### Output

```text
Match Score
Matched Skills
Missing Skills
Skill Gap
Similarity Results
Screening Explanation
Dashboard
```

---

# 💼 Real-World Use Cases

This project can be used as a prototype for:

* Resume screening
* Candidate-job matching
* Recruitment automation
* Applicant filtering
* Skill gap analysis
* HR analytics
* Talent acquisition support
* Job recommendation systems
* Candidate ranking

---

#  Skills Demonstrated : 

This project demonstrates practical experience in:

### Artificial Intelligence

* AI application development
* Intelligent document analysis
* AI-assisted decision support

### Machine Learning

* Feature engineering
* Similarity-based modeling
* Classification
* Model evaluation
* Threshold optimization

### Natural Language Processing

* Text preprocessing
* Text normalization
* TF-IDF
* Sentence embeddings
* Semantic similarity
* Skill extraction
* Resume parsing
* Job Description parsing

### Data Science

* Data processing
* Evaluation datasets
* Pandas
* NumPy
* Performance metrics

### Software Engineering

* Modular Python architecture
* Reusable components
* Unit testing
* Error handling
* Git
* GitHub

### Deployment

* Streamlit
* Docker
* Containerization
* Cloud deployment preparation



#  Limitations

The current system has several limitations:

1. Resume quality and formatting can affect text extraction.
2. Skill extraction depends on the available skill vocabulary/rules.
3. Semantic similarity does not guarantee actual candidate suitability.
4. The evaluation dataset is limited compared with real recruitment data.
5. The reported metrics should not be interpreted as real-world hiring accuracy.
6. Human review is still necessary for actual recruitment decisions.

---



# 🏆 Project Summary

**AI Resume Screening System** is an end-to-end **NLP and Machine Learning portfolio project** designed to automate initial resume screening.

It accepts a resume PDF and manually entered Job Description, extracts and preprocesses text, identifies skills, calculates **TF-IDF and semantic similarity**, combines these signals with skill matching, and produces a final candidate-job match score with skill-gap and explanation features.

The current evaluation achieved:

> **81.00% Accuracy | 100.00% Precision | 76.25% Recall | 86.52% F1 Score**

on the project's evaluation benchmark.

---

# 🔑 Keywords

```text
AI Resume Screening
Resume Parser
Resume Screening System
NLP Resume Screening
Machine Learning
Natural Language Processing
TF-IDF
Cosine Similarity
Semantic Similarity
Sentence Transformers
all-MiniLM-L6-v2
Skill Extraction
Skill Gap Analysis
Candidate Matching
Job Description Matching
Candidate Ranking
Recruitment Automation
HR Tech
Artificial Intelligence
Data Science
Machine Learning Engineer
AI/ML Engineer
NLP Engineer
Python
Scikit-learn
Pandas
NumPy
Streamlit
Docker
Git
GitHub
```

---

# 📄 License

This project is created for **educational, portfolio, and demonstration purposes**.

If you want to make the project open source, an MIT License can be added to the repository.

---

# ⭐ If You Find This Project Useful

If this project helped you understand practical **NLP, Machine Learning, resume screening, semantic similarity, skill extraction, evaluation, Streamlit, and Docker**, consider giving the repository a ⭐ on GitHub.

---

## 👤 Author
**Prathamesh Kasande**

Interested in:
* Artificial Intelligence
* Machine Learning
* NLP
* Data Science
* Generative AI
* Computer Vision

---
