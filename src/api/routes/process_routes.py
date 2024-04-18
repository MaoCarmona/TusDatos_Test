from fastapi import APIRouter, Query
from typing import List

from middlewares.verify_token_routes import VerifyTokenRoute
from database.database import load_json_db

process_router = APIRouter(route_class=VerifyTokenRoute)
processes = load_json_db()

@process_router.get("/process")
async def get_process(limit: int = Query(default=10, ge=1, le=100), offset: int = Query(default=0, ge=0)):
    """
    Retrieve a paginated list of processes.

    Args:
        limit (int, optional): The maximum number of processes to retrieve. Defaults to 10.
            Must be greater than or equal to 1 and less than or equal to 100.
        offset (int, optional): The starting index of the retrieval. Defaults to 0.
            Must be greater than or equal to 0.

    Returns:
        list: A list of processes that is a subset of the `processes` list,
            based on the specified `limit` and `offset` values.
    """
    paginated_processes = processes[offset:offset+limit]

    return paginated_processes

@process_router.get("/process/{id}")
async def get_juicio(id: int):
    """
    Retrieves a process from a list of processes based on its ID.

    Args:
        id (int): The ID of the process to retrieve.

    Returns:
        dict: The process with the specified ID, if found.
        dict: An error message indicating that the process was not found, if no match is found.
    """
    for process in processes:
        if process['id'] == id:
            return process
    return {"error": "process not found"}