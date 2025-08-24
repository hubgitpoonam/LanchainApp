import os

import langsmith
from flask import Flask, request, render_template
from ice_breaker import ice_breaker_with
# 3. Initialize client (project is set via env var)
client = langsmith.Client()  # No project parameter needed



# Create the project explicitly
try:
    client.create_project(project_name="Ice_Breaker")
except langsmith.utils.LangSmithError as e:
    print(f"Project creation skipped: {e}")
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html",error=None)

@app.route('/icebreaker', methods=['POST'])
def icebreaker():
    name = request.form.get("name")
    twitter = request.form.get("twitter")
    result, photo = ice_breaker_with(name, twitter)
    print("Photo URL:", photo) 
    return render_template(
        "index.html",
        summary=result.summary,
        facts=result.facts,
        twitter_insights=getattr(result, "twitter_insights", []),
        photo=photo,
        name=name
    )
if __name__ == '__main__':
    # Debug check
    print("LangSmith Project:", os.getenv("LANGCHAIN_PROJECT"))
    print("LangSmith Tracing Enabled:", os.getenv("LANGCHAIN_TRACING_V2"))
    app.run(host="0.0.0.0", debug=False, port=5003)