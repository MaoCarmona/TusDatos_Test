from fastapi import APIRouter, Query
from typing import List

from middlewares.verify_token_routes import VerifyTokenRoute
from database import load_json_db

process_router = APIRouter(route_class=VerifyTokenRoute)

processes = load_json_db()
@process_router.get("/process")
async def get_process(limit: int = Query(default=10, ge=1, le=100), offset: int = Query(default=0, ge=0)):
    paginated_processes = processes[offset:offset+limit]

    return paginated_processes

@process_router.get("/process/{id}")
async def get_juicio(id: int):
    for process in processes:
        if process['id'] == id:
            return process
    return {"error": "process not found"}