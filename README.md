# AI-TimeMate  
A simple GenAI-powered timesheet automation tool built using Streamlit, SQLite, and Azure OpenAI.

AI-TimeMate allows employees to submit natural-language timesheets and enables managers to review, approve, or reject them with comments. The system uses Azure OpenAI to extract structured JSON from free‑text inputs.

---

## 🚀 Features

### 👨‍💼 Employee Module
- Employee login (demo-friendly dropdown)
- Natural-language timesheet submission
- GenAI extraction using Azure OpenAI
- Automatic JSON generation
- Data stored in SQLite

### 🧑‍💼 Manager Module
- Manager login
- View pending timesheets
- Expandable JSON preview
- Approve / Reject with comments
- Status updates stored in DB

### 🗄️ Backend
- SQLite database (`aitimemate.db`)
- Tables:
  - `employees`
  - `managers`
  - `timesheets`

### 🤖 GenAI Extraction
- Uses Azure OpenAI (GPT‑4o / GPT‑4 Turbo)
- Converts free text → structured JSON
- Extracts:
  - Date
  - Work type (Office / WFH / Leave)
  - Hours
  - Tasks
  - Additional notes

---

## 📁 Project Structure

AI-TimeMate/
│
├── app.py
├── genai_extractor.py
├── azure_config.py        # Not included in repo (contains API keys)
├── aitimemate.db          # Optional
│
└── pages/
├── login.py
├── timesheet_input.py
├── manager_login.py
└── manager_approval.py
