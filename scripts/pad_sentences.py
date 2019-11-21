import argparse

parser = argparse.ArgumentParser(description='Translate with a trained model.')
parser.add_argument('--src', type=str,
                    help='location of the src data')
parser.add_argument('--trg', type=str,
                    help='location of the trg data')
parser.add_argument('--directory', type=str,
                    help='where to put the files')
parser.add_argument('--num_valid', type=int, default=3000)

args = parser.parse_args()

def readf(filename):
    with open(filename) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    return lines

def read_single_line(input_line):
    return input_line.strip().split()

TRG_EPSILON = '@@@@'
SRC_EPSILON = '@@@'
START_PAD = '@str@@'

src_lines = readf(args.src)
trg_lines = readf(args.src)

directory = args.directory
num_valid = args.num_valid

src_out_val = open(directory + "valid_src.txt", 'w')
src_out_train = open(directory + "train_src.txt", 'w')
trg_out_val = open(directory + "valid_trg.txt", 'w')
trg_out_train = open(directory + "train_trg.txt", 'w')

for a in range(len(src_lines)):
    src = src_lines[a].split()
    trg = trg_lines[a].split()

    lenS, lenT = len(src), len(trg)

    # pad at the end,
    # so that both src and trg sequences are of the same size.
    if lenS > lenT:
        src.extend([SRC_EPSILON] * (lenS - lenT))
    elif lenT > lenS:
        trg.extend([TRG_EPSILON] * (lenT - lenS))

    if a < num_valid:
        src_out_val.write(" ".join(src) + '\n')
        trg_out_val.write(" ".join(trg) + '\n')
    else:
        src_out_train.write(" ".join(src) + '\n')
        trg_out_train.write(" ".join(trg) + '\n')