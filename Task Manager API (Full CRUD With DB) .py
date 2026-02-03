from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

# Create DB & table
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

# CREATE
@app.post("/tasks")
def create_task(task: dict):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title) VALUES (?)",
        (task["title"],)
    )
    conn.commit()
    conn.close()
    return {"msg": "Task created"}

# READ ALL
@app.get("/tasks")
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for r in rows:
        tasks.append({
            "id": r[0],
            "title": r[1],
            "completed": bool(r[2])
        })
    return tasks

# READ ONE
@app.get("/tasks/{id}")
def get_task(id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": row[0],
        "title": row[1],
        "completed": bool(row[2])
    }

# UPDATE
@app.put("/tasks/{id}")
def update_task(id: int, task: dict):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title=?, completed=? WHERE id=?",
        (task["title"], int(task["completed"]), id)
    )
    conn.commit()
    conn.close()
    return {"msg": "Task updated"}

# DELETE
@app.delete("/tasks/{id}")
def delete_task(id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"msg": "Task deleted"}
