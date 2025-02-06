import json
import os
import uuid
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from utils import (
    transformer_function,
    check_cached_data
)
from constants import (
    DATA_NOT_PROVIDED,
    CREATED, NOT_FOUND,
    INVALID_FORMAT,
    WRONG_LIST_LENGTH,
    STORAGE_DIRECTORY_NAME,
    CACHE_EXPIRY
)
from database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

STORAGE_DIR = STORAGE_DIRECTORY_NAME
os.makedirs(STORAGE_DIR, exist_ok=True)


@app.on_event("startup")
async def startup():
    redis_url = os.getenv("REDIS_URL")
    try:
        redis = asyncio.from_url(redis_url, encoding="utf-8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis))
    except Exception as ex:
        print("Error connecting to redis:", ex)


class FileSchema(BaseModel):
    """
    Schema for the user input to be mapped on to the model
    """
    list_1: list[str]
    list_2: list[str]


@app.get("/payload/{file_id}/")
async def read_payload(file_id: str):
    """
    GET request to read a stored payload file, transform the lists, and return the result.
    Caching the result to avoid recomputing the transformer function.
    :param file_id:
    :return output_data:
    """
    cache_key = f"read_payload:file_id={file_id}"
    cached_result = await check_cached_data(cache_key)
    if cached_result:
        return json.loads(cached_result)

    file_path = os.path.join(STORAGE_DIR, f"{file_id}.json")

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NOT_FOUND
        )

    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    list_1 = data.get("list_1", [])
    list_2 = data.get("list_2", [])

    merged_output = transformer_function(list_1, list_2)
    output_data = {"output": ", ".join(merged_output)}

    await FastAPICache.get_backend().set(cache_key, json.dumps(output_data), expire=CACHE_EXPIRY)

    return output_data


@app.post("/payload/")
def create_payload(payload: FileSchema):
    """
    POST request to create a json file of exactly 2 list in payload and return the
    UUID of the file.

    :param payload:
    :return new_payload_obj.id:
    """
    if not payload:
        return HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=DATA_NOT_PROVIDED
        )

    if not isinstance(payload.dict(), dict):
        return HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INVALID_FORMAT
        )

    lists = [v for v in payload.dict().values() if isinstance(v, list)]
    if len(lists) != 2:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=WRONG_LIST_LENGTH
        )

    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(STORAGE_DIR, f"{file_id}.json")

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(payload.dict(), json_file, indent=4)

        return {"message": CREATED, "data": {"id": file_id}}

    except Exception as ex:
        return HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Unexpected error: " + str(ex)
        )
