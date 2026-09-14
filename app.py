from flask import Flask, jsonify
import socket
import psycopg2
import os

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host="db",
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    
     


@app.route("/")
def home():
    return f"""
    <h1>NEXUS 🚀</h1>
    <p>Scalable Cloud Infrastructure & Application Platform</p>
    <p>Status: Online</p>
    <p>Server: {socket.gethostname()}</p>
    """


@app.route("/health")
def health():
    try:
        connection = get_db_connection()
        connection.close()
        database_status = "connected"
    except Exception:
        database_status = "error"

    return jsonify({
        "status": "healthy",
        "service": "nexus",
        "version": "1.0",
        "server": socket.gethostname(),
        "database": database_status
    })


@app.route("/data")
def data():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL
        )
    """)

    cursor.execute(
        "INSERT INTO messages (message) VALUES (%s) RETURNING id",
        ("NEXUS database is working!",)
    )

    new_id = cursor.fetchone()[0]

    connection.commit()

    cursor.execute("SELECT id, message FROM messages ORDER BY id")

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({
        "inserted_id": new_id,
        "messages": [
            {"id": row[0], "message": row[1]}
            for row in rows
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
