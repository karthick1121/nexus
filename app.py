from flask import Flask, jsonify
import socket
import psycopg2

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="nexus",
        user="nexus",
        password="nexuspass"
    )


@app.route("/")
def home():
    hostname = socket.gethostname()

    return f"""
    <h1>NEXUS 🚀</h1>
    <p>Scalable Cloud Infrastructure & Application Platform</p>
    <p>Status: Online</p>
    <p>Server: {hostname}</p>
    """


@app.route("/health")
def health():
    try:
        connection = get_db_connection()
        connection.close()

        database_status = "connected"
    except Exception as e:
        database_status = "error"

    return jsonify({
        "status": "healthy",
        "service": "nexus",
        "version": "1.0",
        "server": socket.gethostname(),
        "database": database_status
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
