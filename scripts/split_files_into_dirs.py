import sys
import os

if len(sys.argv) < 3:
    print("Error: Please specify directory and number of files per directory")

src_dir = sys.argv[1]
num_dirs = sys.argv[2]

for file in sorted(os.listdir(src_dir)):
    print(file)