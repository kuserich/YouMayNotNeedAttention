import sys

DELIMITER = ' ||| '

file_handler = open(sys.argv[1], "r")
new_file = open(sys.argv[1] + "_new", "a")
new_src = open(sys.argv[1] + "_new.src", "a")
new_trg = open(sys.argv[1] + "_new.trg", "a")
lines = file_handler.readlines()

counter = 0
for index, line in enumerate(lines):
    split_line = line.split(DELIMITER)
    # check split_line[1] for length 1 because it usually contains the newline character
    if len(split_line) != 2 or len(split_line[0]) == 0 or len(split_line[1]) == 0 or len(split_line[1]) == 1:
        print(index)
        counter += 1
    else:
        new_file.write(line)
        new_src.write(split_line[0] + '\n')
        new_trg.write(split_line[1])

print("Found %d invalid lines" % counter)
print("Total lines: %d" % len(lines))
