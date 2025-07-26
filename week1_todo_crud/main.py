from fastapi import FastAPI, HTTPException,Form, Depends
from fastapi.responses import JSONResponse
from Utils import Utils, configs
from models import Task, FilterParams,LoginModel,SignupModel
from typing import  Annotated,List

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/tasks/", response_model=List[Task])
def read_task(
    filter_params: Annotated[FilterParams, Depends()]
):
    tasks = Utils.get_todo_list()
    tasks = tasks[filter_params.skip : filter_params.skip + filter_params.limit]
    
    if filter_params.order_by == "asc":
        tasks = sorted(tasks, key=lambda x: x["id"])
    elif filter_params.order_by == "desc":
        tasks = sorted(tasks, key=lambda x: x["id"], reverse=True)

    return tasks


@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    try:
        return Utils.add_todo_item(task)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
   return Utils.update_todo_item(task_id, updated_task)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        Utils.remove_todo_item(task_id)
        return JSONResponse(status_code=204, content=None)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@app.post("/login")
def login(data: Annotated[LoginModel,Form]):
    credentials = data.model_dump(exclude={"confirm_password"})
    users = Utils.load_json(configs.User_DATABASE_FILE)
    
    for user in users:
        username_match = user.get("username") == credentials.get("username")
        email_match = user.get("email") == credentials.get("email")
        password_match = user.get("password") == credentials.get("password")

        if (username_match or email_match) and password_match:
            return JSONResponse(status_code=200, content={"message": "Login successful"})

    # If loop completes with no match
    raise HTTPException(status_code=400, detail="Invalid credentials or user does not exist")
        

@app.post("/signup")
def signup(data: Annotated[SignupModel,Form]):
    credentials = data.model_dump(exclude={"confirm_password"})
    users = Utils.load_json(configs.User_DATABASE_FILE)
    if credentials in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users.append(credentials)
    Utils.save_json(configs.User_DATABASE_FILE, users)
    return JSONResponse(status_code=201, content={"message": "User created successfully"}) 