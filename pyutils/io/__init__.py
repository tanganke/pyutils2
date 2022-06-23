

def human_readable_size(size, decimal_places=3) -> str:
    """
    convert bytes to human readable string

    Args:
        size : number of bytes
        decimal_places (int, optional): Defaults to 3.

    Returns:
        str: human readable string
    """
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f}{unit}"
