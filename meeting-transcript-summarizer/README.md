````markdown
# 📝 Meeting Transcript Summarizer & Action Item Extractor

This project automates the process of summarizing meeting transcripts and extracting actionable items using Azure OpenAI's `gpt-4o-mini` model. It provides a Flask-based web interface and ensures JSON validation using Pydantic.

---

## 🔧 Features

- Summarizes meeting transcript into **2 sentences**
- Extracts all **action items as dash-prefixed bullet points**
- Returns clean, valid **JSON output**
- Built-in **retry logic** for malformed outputs
- Supports **Flask UI** for input/output visualization
- Azure-native using `azure-openai` SDK

---

## 🧠 Sample Output Format

```json
{
  "summary": "Meeting focused on marketing campaign and asset delivery timelines. Action items include finalizing drafts, delivering assets, and submitting budget requests.",
  "action_items": [
    "- Emma will share the social campaign draft today.",
    "- Frank will ensure the design team delivers assets by Tuesday.",
    "- Emma will schedule the ads for next week once the assets are received.",
    "- Team members need to submit their budget requests before the end of the day.",
    "- The host will send out the final budget spreadsheet."
  ]
}
````

---

## 📂 Project Structure

```
├── app.py                  # Flask application
├── meeting_notes.py        # Core logic for prompt creation and API call. Pydantic model for JSON validation
├── transcripts.txt         # Input transcripts (for demo/testing)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ⚙️ Environment Variables

Set these in your `.env` file or environment:

```env
AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_DEPLOYMENT=<your-deployment-name>  # e.g. gpt-4o-mini
```

---

## 🚀 Run the App

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Flask Server

```bash
python app.py
```

Access at [http://localhost:5000](http://localhost:5000)

---

## 📜 Usage

* Input a raw meeting transcript (with or without speaker names).
* Click "Submit".
* View summary and structured action items in JSON.
* Retry logic ensures robust parsing if LLM output fails.

---

## 🧪 Sample Transcripts

Transcripts can be edited or extended via the `transcripts.txt` file.

---

## ✅ Dependencies

* `flask`
* `python-dotenv`
* `pydantic`
* `openai`

---

## 🛡️ Notes

* Uses `temperature=0` for deterministic output
* Retries once if JSON parsing fails
* Handles both `json.JSONDecodeError` and Pydantic `ValidationError`

---

## 👨‍💻 Author

Built by a Bharadwaj using GPT-4o-mini and Flask. Feel free to fork and extend!

```

---
```

