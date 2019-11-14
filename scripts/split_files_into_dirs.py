import sys
import os
import math

if len(sys.argv) < 3:
    print("Error: Please specify directory and number of files per directory")

src_dir = sys.argv[1]
num_dirs = int(sys.argv[2])

num_files = len([file for file in os.listdir(src_dir)])
num_files_per_dir = math.floor(num_files / num_dirs)

print("INFO: There are %s files in '%s'" % (num_files, src_dir))
print("INFO: %s directories will be created with %d files each" % (num_dirs, num_files_per_dir))


dir_cnt = 0
file_cnt = 0
for file in sorted(os.listdir(src_dir)):
    if file_cnt % num_files_per_dir == 0:
        file_cnt = 0
        dir_cnt += 1

        if not os.path.exists(os.path.join(src_dir, str(dir_cnt))):
            os.makedirs(os.path.join(src_dir, str(dir_cnt)))

    file_cnt += 1

    os.move(os.path.join(os.path.join(src_dir, str(dir_cnt)), file))
