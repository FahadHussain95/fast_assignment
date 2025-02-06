import json
import os
import uuid
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from utils import transformer_function
from constants import (
    DATA_NOT_PROVIDED,
    CREATED, NOT_FOUND,
    INVALID_FORMAT,
    WRONG_LIST_LENGTH,
    STORAGE_DIRECTORY_NAME
)
from database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

STORAGE_DIR = STORAGE_DIRECTORY_NAME
os.makedirs(STORAGE_DIR, exist_ok=True)


class FileSchema(BaseModel):
    """
    Schema for the user input to be mapped on to the model
    """
    list_1: list[str]
    list_2: list[str]


@app.get("/payload/{file_id}/")
def read_payload(file_id: str):
    """
    GET request to read a stored payload file, transform the lists, and return the result.

    :param file_id: The unique identifier of the stored JSON file.
    :return: Transformed and merged list as a string.
    """
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

    return {"output": ", ".join(merged_output)}


@app.post("/payload/")
def create_payload(payload: FileSchema):
    """
    POST request to create a json file of exactly 2 list in payload and return the UUID of the file

    :param payload:
    :param db:
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