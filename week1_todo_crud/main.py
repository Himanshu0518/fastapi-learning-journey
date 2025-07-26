from fastapi import FastAPI, HTTPException,Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import  Optional, Annotated


from Utils import Utils,configs

app = FastAPI()

class Task(BaseModel):
    id: int
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: Annotated[str, Field(min_length=1, max_length=200)]
    completed: bool = False

class FilterParams(BaseModel):
    skip: Annotated[int, Query(ge=0, description="Items to skip")] = 0
    limit: Annotated[int, Query(ge=1, le=100, description="Items to return")] = configs.DB_LEN
    order_by: Optional[str] = Query(None, pattern="^(asc|desc)$")

@app.get("/")
def read_root():
    return {"Hello": "World"}


from typing import List

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
