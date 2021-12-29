from flask import Flask, request, jsonify, render_template
import index

app = Flask(__name__)

index.create_index()

@app.route("/")
def query_search():
    query = request.args.get("query")

    if not query:
        return jsonify({"error": "query parameter is required"}), 400

    results = index.search(query)

    return jsonify({"query": query, "results": results})

@app.route("/autocomplete")
def autocomplete_view():
    query = request.args.get("query")

    if not query:
        return jsonify({"error": "query parameter is required"}), 400

    results = index.get_autocomplete_list(query)

    return jsonify({"query": query, "results": list(results)})

@app.route("/search")
def user_search():
    return render_template("search.html")

app.run()