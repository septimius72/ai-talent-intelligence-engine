# AI Talent Intelligence & Sourcing Engine

A lightweight, Python based recruiting automation toolkit built with the **Google GenAI SDK (`gemini-2.5-flash`)** and **Pydantic**. Designed to eliminate manual top of funnel triage, discover open-source AI builders on GitHub, and generate structured candidate calibration sheets for technical hiring managers.

## 🎯 Why I Built This
High stakes technical recruiting especially across **Agentic AI, ML/Data, Security, and Product** fails when recruiters rely on generic keyword matching. This repository demonstrates a pragmatic "AI assisted, human finished" workflow:
1. **Automated Discovery (`github_ai_sourcer.py`):** Queries the GitHub REST API for active contributors in specific technical ecosystems (e.g., MCP servers, Python agent frameworks), summarizes their repositories, and uses Gemini to score relevance and draft technical outreach hooks.
2. **Structured Rubric Calibration (`batch_profile_scorer.py`):** Ingests exported candidate CSVs (from LinkedIn Recruiter or Lever ATS), evaluates each profile against a strict hiring rubric using **Pydantic structured JSON outputs**, and exports a ranked shortlist with tailored interview questions.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **LLM & SDK:** Google GenAI SDK (`google-genai`, `gemini-2.5-flash`)
* **Data Validation & Parsing:** `pydantic`, `pandas`
* **External APIs:** GitHub REST API (`requests`)

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install google-genai requests pandas pydantic
```

### 2. Configure Your API Key
Keep credentials out of source control by setting your Gemini API key as an environment variable:

* **macOS / Linux:**
  ```bash
  export GEMINI_API_KEY="your_api_key_here"
  ```
* **Windows (PowerShell):**
  ```powershell
  \$env:GEMINI_API_KEY="your_api_key_here"
  ```

### 3. Run the Pipelines
* **Discover & score open source AI builders:**
  ```bash
  python github_ai_sourcer.py
  ```
  *Outputs `sourced_ai_builders.csv`.*

* **Batch score a candidate CSV against a hiring rubric:**
  ```bash
  python batch_profile_scorer.py
  ```
  *Reads `candidates_input.csv` and outputs `calibrated_shortlist.csv`.*

---

## 🔒 Data Privacy & Governance Note
In production recruiting environments, candidate PII is handled strictly in compliance with enterprise data governance policies using zero-data-retention enterprise API endpoints and anonymizing personally identifiable fields prior to batch evaluation.

---

## 👤 Author
**Alexander Becz** — Senior/Staff Technical Recruiter & Talent Strategist  
[LinkedIn](https://linkedin.com) | [Portfolio](https://weebly.com)
