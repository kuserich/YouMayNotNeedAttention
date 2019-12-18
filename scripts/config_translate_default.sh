CUDA_VISIBLE_DEVICES=0

# Model and corpus of base line Press & Smith Model
MODEL="exps-10-22/20191025-161111/model390000.pt"
DATA="data/10-25-align-eps/corpus"

SRC_PATH="/srv/scratch1/goeckeritz/dev.bpe.en"
TARGET_TRANSLATION="sockeye_autopilot/systems/wmt14_en_de/data/tst/dev.trg"
BEAM_SIZES=(5)
EPSILON_LIMITS=(3)
SRC_EPSILON_INJECTIONS=(9)
START_PADS=(4)
LANGUAGE="de"
SAVE_DIR="output/"
FILE_NAME=""
PREFIX=""
SUFFIX=""
MODEL_CLASS="default"