import sys

SRC_EPSILON = "@@@@"
TRG_EPSILON = "@@@"

src_f = sys.argv[1]
trg_f = sys.argv[2]

src_o = open(src_f, 'r')
trg_o = open(trg_f, 'r')

src = src_o.readlines()
trg = trg_o.readlines()

for i in range(len(src)):
    s = src[i].split()[-1]
    t = trg[i].split()[-1]
    if ((s == SRC_EPSILON and t == TRG_EPSILON)
            or (t == SRC_EPSILON and s == SRC_EPSILON)):
        print(i)
        print('\t'+src[i])
        print('\t'+trg[i])
