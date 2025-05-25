from flask import Flask, render_template_string
from meeting_notes import extract_meeting_notes  # Replace with actual import
import json

app = Flask(__name__)

def load_transcripts(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return [transcript.strip() for transcript in content.split('---') if transcript.strip()]

@app.route("/")
def index():
    results = []
    # Load sample transcripts from a file
    sample_transcripts = load_transcripts("transcripts.txt")
    
    for idx, transcript in enumerate(sample_transcripts, 1):
        try:
            notes = extract_meeting_notes(transcript)
            results.append({
                "id": idx,
                "summary": notes["summary"],
                "action_items": notes["action_items"],
                "transcript": transcript.strip()
            })
        except Exception as e:
            results.append({
                "id": idx,
                "summary": "Error processing this transcript.",
                "action_items": [],
                "transcript": transcript.strip()
            })

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Meeting Notes</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background: #f7f9fa; }
            .card { background: #fff; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            h2 { margin-top: 0; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>Meeting Transcript Summarizer</h1>
        {% for item in results %}
        <div class="card">
            <h2>Transcript {{ item.id }}</h2>
            <strong>Transcript:</strong>
            <pre>{{ item.transcript }}</pre>
            <strong>Summary:</strong>
            <p>{{ item.summary }}</p>
            <strong>Action Items:</strong>
            <ul>
                {% for action in item.action_items %}
                <li>{{ action }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html_template, results=results)

if __name__ == "__main__":
    app.run(debug=True)
