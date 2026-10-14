def cookie(x):
    if isinstance(x, str):
        eater = "Zach"
    elif isinstance(x, bool):
        eater = "the dog"
    elif isinstance(x, (int, float)):
        eater = "Monica"
    else:
        eater = "the dog"

    return f"Who ate the last cookie? It was {eater}!"
