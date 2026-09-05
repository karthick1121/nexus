from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>NEXUS 🚀</h1>
    <p>Scalable Cloud Infrastructure & Application Platform</p>
    <p>Status: Online</p>
    """


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "nexus",
        "version": "1.0"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)