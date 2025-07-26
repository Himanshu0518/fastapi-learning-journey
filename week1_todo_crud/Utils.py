import json
from fastapi import  HTTPException
from fastapi.responses import JSONResponse
import os
from dataclasses import dataclass

DATABASE_FILE = 'task_db.json'
if not os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE, 'w') as f:
        json.dump([], f)

def db_len():
    """
    Returns the length of the todo list in the database.
    """
    with open(DATABASE_FILE, 'r') as f:
        tasks = json.load(f)
    return len(tasks)


@dataclass
class configs:
    DATABASE_FILE: str = DATABASE_FILE
    DB_LEN : int = db_len()
    User_DATABASE_FILE: str = 'user_db.json'
    if not os.path.exists(User_DATABASE_FILE):
        with open(User_DATABASE_FILE, 'w') as f:
            json.dump([], f)

class Utils:
    @staticmethod
    def get_todo_list():
        """
        Returns a list of todo items.
        """
        try:
            with open(DATABASE_FILE, 'r') as f:
              tasks = json.load(f)
            return tasks
        except FileNotFoundError:
            return []
        

    @staticmethod
    def add_todo_item(task):
        """
        Adds a todo item to the list.
        """
        with open(DATABASE_FILE, 'r') as f:
                tasks = json.load(f)

            # Check if ID already exists
        if any(t['id'] == task.id for t in tasks):
                raise HTTPException(status_code=400, detail="Task ID already exists")

            
        tasks.append(task.dict())
        with open(DATABASE_FILE, 'w') as f:
                json.dump(tasks, f, indent=4)
        return task
        

    @staticmethod
    def remove_todo_item(task_id):
        """
        Removes a todo item from the list.
        """
        
        with open(DATABASE_FILE, 'r') as f:
            tasks = json.load(f)

        for i, task in enumerate(tasks):
            if task['id'] == task_id:
                del tasks[i]
                with open(DATABASE_FILE, 'w') as f:
                    json.dump(tasks, f, indent=4)
                return {"message": "Task deleted successfully"}

        raise HTTPException(status_code=404, detail="Task not found")
    @staticmethod
    def update_todo_item(task_id, updated_task):
        """
        Updates an existing todo item.
        """
        with open(DATABASE_FILE, 'r') as f:
           tasks = json.load(f)

        for index, task in enumerate(tasks):
            if task['id'] == task_id:
                tasks[index] = updated_task.dict()
                with open(DATABASE_FILE, 'w') as f:
                    json.dump(tasks, f, indent=4)
                return updated_task

        raise HTTPException(status_code=404, detail="Task not found")

    @staticmethod
    def  load_json(file_path):
        """
        Loads a JSON file and returns its content.
        """
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(file_path, 'r') as f:
            return json.load(f)
        
    @staticmethod
    def save_json(file_path, data):
        """
        Saves data to a JSON file.
        """
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)