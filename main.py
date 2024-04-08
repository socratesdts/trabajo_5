# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4

app = FastAPI()

# Modelo para el registro de usuarios
class User(BaseModel):
    id: Optional[UUID] = None
    username: str
    email: str
    password: str

# Modelo para las tareas
class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: str
    status: str  # Podría ser una enumeración para 'pendiente', 'en progreso', 'completada'
    user_id: UUID

# Almacenamiento en memoria para simplificar el ejemplo
users = {}
tasks = {}

# Registro de usuarios
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: User):
    user.id = uuid4()
    if user.id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user.id] = user
    return {"message": "User registered successfully", "user_id": user.id}

# Obtener datos de usuario
@app.get("/user/{user_id}")
def get_user(user_id: UUID):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

# Crear tarea
@app.post("/tasks/create", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    task.id = uuid4()
    if task.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    tasks[task.id] = task
    return {"message": "Task created successfully", "task_id": task.id}

# Listar tareas por usuario
@app.get("/tasks/{user_id}", response_model=List[Task])
def list_tasks_by_user(user_id: UUID):
    user_tasks = [task for task in tasks.values() if task.user_id == user_id]
    return user_tasks


