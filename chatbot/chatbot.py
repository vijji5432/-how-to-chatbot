from flask import Flask, render_template, request, jsonify
from fetch_process import fetch_and_match  # Make sure this is the updated fetch_process.py with FAISS

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def chat():
    query = request.json.get("query")  # Change from 'msg' to 'query'
    platform = request.json.get("platform")
    if not query or not platform:
        return jsonify({"error": "Both 'query' and 'platform' are required."}), 400

    # Fetch the relevant content based on the query and platform using the FAISS search
    response = get_chat_response(query, platform)
    return jsonify({"response": response})

def get_chat_response(query, platform):
    # Fetch and match the query with documentation for the specified platform using FAISS
    relevant_content = fetch_and_match(query, platform)

    # Check if there's an error or no relevant content found
    if isinstance(relevant_content, dict) and "error" in relevant_content:
        return [{"content": relevant_content["error"]}]

    # Prepare response as a list of dictionaries with URL and content
    readable_response = [
        {"url": url, "content": content[:500]}  # Limit each section to 500 characters for readability
        for url, content in relevant_content.items()
    ]

    return readable_response

if __name__ == "__main__":
    app.run(debug=True)
