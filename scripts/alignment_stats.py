import sys

if len(sys.argv) < 2:
    print("Error: Please add the path to the alignment file as an argument.")
    exit()

alignments_file = sys.argv[1]
with open(alignments_file) as file:
    for line in file:
        print(line)
        exit()
