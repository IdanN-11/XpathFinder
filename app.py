from flask import Flask, render_template, request, jsonify
from xpath_finder import generate_xpaths

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    # Get data from the form
    html_doc = request.form.get("html_doc", "")  # HTML content
    prompt = request.form.get("prompt", "")      # Prompt for Grok
    website_url = request.form.get("website_url", "")  # optional live URL
    extra_text = request.form.get("extra_context", "") # optional extra context

    try:
        # Call generate_xpaths with proper variables
        result = generate_xpaths(
            html_doc=html_doc,
            prompt=prompt,
            extra_context=extra_text,
            test_url=website_url if website_url else None
        )

        return jsonify(result)
    except Exception as e:
        # Catch any errors and return as JSON
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    # Run Flask app
    app.run(debug=True)
