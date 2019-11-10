import os
import sys

directory = sys.argv[1]

for file in os.listdir(directory):
    if file.endswith(".bleu"):
        with open(os.path.join(directory, file)) as bleu_file:
            print(bleu_file.readlines())
