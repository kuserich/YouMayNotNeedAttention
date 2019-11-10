import os
import sys

directory = sys.argv[1]

for file in os.listdir(directory):
    if file.endswith(".bleu"):
        print(os.path.join(directory, file))
