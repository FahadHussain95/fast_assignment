import json

from fastapi_cache import FastAPICache
from sqlalchemy.exc import SQLAlchemyError

from models import CachedData


def transformer_function(list_1, list_2):
    """
    Transforms two lists by interleaving their elements and converting in uppercase.
    """
    merged_output = []
    for pair in zip(list_1, list_2):
        merged_output.extend(map(str.upper, pair))

    longer_list = list_1 if len(list_1) > len(list_2) else list_2
    merged_output.extend([item.upper() for item in longer_list[len(merged_output) // 2:]])

    return merged_output


async def check_cached_data(cache_key):
    """
    Check cached data by using unique cache key.
    """
    return await FastAPICache.get_backend().get(cache_key)


def check_data_in_db(db, file_id):
    """
    If cache data not found, this function checks the same in db using the unique file_id.
    """
    return db.query(CachedData).filter(CachedData.file_id == file_id).first()


def store_data_in_db(db, file_id, output_data):
    """
    This function saves the cached data into the db table.
    """
    try:
        db_entry = CachedData(file_id=file_id, data=output_data)
        db.add(db_entry)
        db.commit()
    except SQLAlchemyError as ex:
        db.rollback()
        print(f"An error occurred while storing data in db: {ex}")
