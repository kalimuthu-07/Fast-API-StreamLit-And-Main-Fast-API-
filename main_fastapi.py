
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import mysql.connector
from fastapi import HTTPException

app = FastAPI()


class ToDoItem(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kali@0609",
        database="todo_db"
    )


@app.post("/todos/")
def create_todo(item: ToDoItem):
    conn = get_db_connection()
    cursor = conn.cursor()

    
    query = """
        INSERT INTO todos (title, description, completed)
        VALUES (%s, %s, %s)
    """
    values = (item.title, item.description, item.completed)
    cursor.execute(query, values)
    conn.commit()

    
    todo_id = cursor.lastrowid

    
    cursor.close()
    conn.close()

    
    return {
        "id": todo_id,
        "title": item.title,
        "description": item.description,
        "completed": item.completed
    }

@app.get("/todos/")
def read_all_todos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM todos"
    cursor.execute(query)
    todos = cursor.fetchall()

    cursor.close()
    conn.close()

    return todos


@app.get("/todos/{todo_id}")
def read_todo(todo_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM todos WHERE id = %s"
    cursor.execute(query, (todo_id,))
    todo = cursor.fetchone()

    cursor.close()
    conn.close()

    if todo is None:
        raise HTTPException(status_code=404, detail=f"ToDo item with ID {todo_id} not found")

    return todo
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, item: ToDoItem):
    conn = get_db_connection()
    cursor = conn.cursor()

    
    cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
    existing = cursor.fetchone()

    if existing is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail=f"ToDo item with ID {todo_id} not found")

    
    update_query = """
        UPDATE todos
        SET title = %s, description = %s, completed = %s
        WHERE id = %s
    """
    values = (item.title, item.description, item.completed, todo_id)
    cursor.execute(update_query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": todo_id,
        "title": item.title,
        "description": item.description,
        "completed": item.completed
    }

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    
    cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
    existing = cursor.fetchone()

    if existing is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail=f"ToDo item with ID {todo_id} not found")

    
    cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": f"ToDo item with ID {todo_id} has been deleted"}
