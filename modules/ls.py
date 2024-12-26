import os

def run() -> str:
    print('Running ls module ..')
    data = '\n'.join(os.listdir('.'))
    return data
