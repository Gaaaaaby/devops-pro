import os
import sqlite3

import redis
from fastapi import FastAPI

DB_PATH = os.getenv("DB_PATH", "tasks.db")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

app = FastAPI(title="DevOps Pro API")


# conexión a SQLite
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# conexión a Redis
def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


# inicializar tabla
def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


@app.get("/")
def read_root():
    return {"message": "DevOps avanzado, todo gratis"}


@app.get("/health")
def health():
    r = get_redis()
    try:
        r.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "down"

    conn = get_db()
    try:
        conn.execute("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "down"
    finally:
        conn.close()

    return {"status": "ok", "db": db_status, "redis": redis_status}


@app.post("/tasks")
def create_task(title: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    task_id = cur.lastrowid
    conn.close()
    return {"id": task_id, "title": title}


@app.get("/tasks")
def list_tasks():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM tasks")
    rows = cur.fetchall()
    conn.close()
    return [{"id": row["id"], "title": row["title"]} for row in rows]


@app.get("/counter")
def counter():
    r = get_redis()
    value = r.incr("counter")
    return {"counter": value}
