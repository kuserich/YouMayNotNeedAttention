import sys

if len(sys.argv) < 2:
    print("Error: Please add the path to the alignment file as an argument.")
    exit()


def split_fast_align_pair(aStr):
    parts = aStr.split('-')
    return (int(parts[0], 10), int(parts[1], 10))


def sum(a, b):
    return a + b

alignments_file = sys.argv[1]
pair_distances = []
line_distances = []
total_distance = 0
total_num_words = 0
with open(alignments_file) as file:
    for line in file:
        line_distance = 0
        words = line.split()
        for pair in words:
            i, j = split_fast_align_pair(pair)
            distance = abs(i - j)
            line_distance += distance
            total_distance += distance
            pair_distances.append(distance)
        line_distances.append(line_distance)
        total_num_words += len(words)

average_pair_distance = reduce(sum, pair_distances) / len(pair_distances)
average_line_distance = reduce(sum, line_distances) / len(line_distances)

print("")
print("ALIGNMENT STATISTICS")
print("=========================")
print("Number of Lines: %d" % len(line_distances))
print("Number of Words: %d" % total_num_words)
print("Total Distance: %d" % total_distance)
print("Average Pair Distance: %d" % average_pair_distance)
print("Average Line Distance: %d" % average_line_distance)
print("")
