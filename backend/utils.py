
def transformer_function(list_1, list_2):
    """
    Transforms two lists by interleaving their elements in uppercase.

    :param list_1: First list of strings
    :param list_2: Second list of strings
    :return: Transformed and merged list
    """
    merged_output = []
    for pair in zip(list_1, list_2):
        merged_output.extend(map(str.upper, pair))

    longer_list = list_1 if len(list_1) > len(list_2) else list_2
    merged_output.extend([item.upper() for item in longer_list[len(merged_output) // 2:]])

    return merged_output
