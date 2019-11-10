import os
import sys
import json

directory = sys.argv[1]

for file in os.listdir(directory):
    if file.endswith(".bleu"):
        with open(os.path.join(directory, file), "r") as bleu_file:
            data = json.loads(bleu_file.readline())
            print(data["score"])
