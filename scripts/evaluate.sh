SCRIPTS_DIR=`dirname "$0"`
BASE_DIR=${SCRIPTS_DIR}/..

source ${SCRIPTS_DIR}/config.sh

export CUDA_VISIBLE_DEVICES=2

MODEL="exps/model390000.pt"
DATA="corpus/WMTENDE/4pad"
#SRC_PATH="sockeye_autopilot/systems/wmt14_en_de/data/bpe/test.0.src"
SRC_PATH="sockeye_autopilot/systems/wmt14_en_de/data/bpe/dev.src"
#BEAM_SIZES=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35)
BEAM_SIZES=(7 8)
#TARGET_TRANSLATION="sockeye_autopilot/systems/wmt14_en_de/data/tst/test.0.trg"
TARGET_TRANSLATION="sockeye_autopilot/systems/wmt14_en_de/data/tst/dev.trg"
EPSILON_LIMITS=(4 5 6)
SRC_EPSILON_INJECTION=4
START_PADS=(3 4)
LANGUAGE="de"
SAVE_DIR="output/"
FILE_NAME="translation_test.txt"

name=$(date +"%m-%d-%y")


for BEAM_SIZE in "${BEAM_SIZES[@]}"
do
    for START_PAD in "${START_PADS[@]}"
        do
            for EPSILON_LIMIT in "${EPSILON_LIMITS[@]}"
            do
                file_name="${name}_beam_${BEAM_SIZE}_pads_${START_PAD}_epsilon_limit_${EPSILON_LIMIT}.txt"
                mkdir -p ${SAVE_DIR}
                python model/generate.py \
                      --checkpoint ${MODEL} \
                      --data ${DATA} \
                      --src_path ${SRC_PATH} \
                      --beam_size ${BEAM_SIZE} \
                      --eval \
                      --target_translation ${TARGET_TRANSLATION} \
                      --epsilon_limit ${EPSILON_LIMIT} \
                      --src_epsilon_injection ${SRC_EPSILON_INJECTION} \
                      --start_pads ${START_PAD} \
                      --language ${LANGUAGE} \
                      --save_dir ${SAVE_DIR} \
                      --file_name ${file_name} &
                echo "Generated output for START_PADS=${START_PAD} and BEAM_SIZE=${BEAM_SIZE} and EPSILON_LIMIT=${EPSILON_LIMIT}"
                done
        done
done

