from fastapi_cache import FastAPICache


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
    return await FastAPICache.get_backend().get(cache_key)
