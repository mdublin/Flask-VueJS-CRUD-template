import os

with open('environ.txt', 'w') as f:
    for key in os.environ.keys():
        f.write(key + "\n")

os.environ[key]





