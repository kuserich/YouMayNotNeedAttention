import sys

print(sys.argv)

if len(sys.argv) < 2:
    print("Error: Please add the path to the alignment file as an argument.")
    exit()


def split_fast_align_pair(aStr):
    parts = aStr.split('-')
    return (int(parts[0], 10), int(parts[1], 10))

alignments_file = sys.argv[1]
distance = 0
with open(alignments_file) as file:
    for line in file:
        for pair in line.split():
            #i, j = split_fast_align_pair(line)
            #distance += abs(int(i, 10) - int(j, 10))
            #print(line, distance)
            print(pair)
        exit()
