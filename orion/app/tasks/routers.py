from fastapi import APIRouter

router = APIRouter(
    tags=["tasks"],
)

@router.get("/tasks",)
async def read_tasks():
    return [{"task_id": 1, "name": "Sample Task"}]