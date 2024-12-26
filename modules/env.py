import os

def run() -> str:
    data = '\n'.join([f'{key}: {val}' for key, val in os.environ.items()])
    return data
