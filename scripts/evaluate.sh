SCRIPTS_DIR=`dirname "$0"`
BASE_DIR=${SCRIPTS_DIR}/..

source ${SCRIPTS_DIR}/config.sh

MODEL="exps/model390000.pt"
DATA="corpus/WMTENDE/4pad"
# SRC_PATH="sockeye_autopilot/systems/wmt14_en_de/data/bpe/test.0.src"
SRC_PATH="sockeye_autopilot/systems/wmt14_en_de/data/bpe/dev.src"
BEAM_SIZE=5
# TARGET_TRANSLATION="sockeye_autopilot/systems/wmt14_en_de/data/tst/test.0.trg"
TARGET_TRANSLATION="sockeye_autopilot/systems/wmt14_en_de/data/tst/dev.trg"
EPSILON_LIMIT=3
SRC_EPSILON_INJECTION=4
START_PADS=5
LANGUAGE="de"
SAVE_DIR="output/"

python model/generate.py \
    --checkpoint ${MODEL} \
    --data ${DATA} \
    --src_path ${SRC_PATH} \
    --beam_size ${BEAM_SIZE} \
    --eval \
    --target_translation ${TARGET_TRANSLATION} \
    --epsilon_limit ${EPSILON_LIMIT} \
    --src_epsilon_injection ${SRC_EPSILON_INJECTION} \
    --start_pads ${START_PADS} \
    --language ${LANGUAGE} \
    --save_dir ${SAVE_DIR}
