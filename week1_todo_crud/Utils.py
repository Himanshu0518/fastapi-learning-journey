import json
from fastapi import  HTTPException
from fastapi.responses import JSONResponse
import os
from dataclasses import dataclass

DATABASE_FILE = 'database.json'
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

        