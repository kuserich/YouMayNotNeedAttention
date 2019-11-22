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
EOS = '<eos>'

src_lines = readf(args.src)
trg_lines = readf(args.trg)

directory = args.directory
num_valid = args.num_valid

src_out_val = open(directory + "valid_src.txt", 'w')
src_out_train = open(directory + "train_src.txt", 'w')
trg_out_val = open(directory + "valid_trg.txt", 'w')
trg_out_train = open(directory + "train_trg.txt", 'w')

for a in range(len(src_lines)):
    src = src_lines[a].split()
    trg = trg_lines[a].split()

    if src[0] == EOS:
        del src[0]
    if src[-1] == EOS:
        del src[-1]

    if trg[0] == EOS:
        del trg[0]
    if trg[-1] == EOS:
        del trg[-1]

    lenS, lenT = len(src), len(trg)

    # pad at the end,
    # so that both src and trg sequences are of the same size.
    if lenS < lenT:
        src.extend([SRC_EPSILON] * (lenT - lenS))
    elif lenT < lenS:
        trg.extend([TRG_EPSILON] * (lenS - lenT))

    if a < num_valid:
        src_out_val.write(" ".join(src) + '\n')
        trg_out_val.write(" ".join(trg) + '\n')
    else:
        src_out_train.write(" ".join(src) + '\n')
        trg_out_train.write(" ".join(trg) + '\n')