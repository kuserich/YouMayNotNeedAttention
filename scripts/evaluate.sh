SCRIPTS_DIR=`dirname "$0"`
BASE_DIR=${SCRIPTS_DIR}/..

source ${SCRIPTS_DIR}/config.sh

export CUDA_VISIBLE_DEVICES=2

MODEL="exps-10-22/20191025-161111/model390000.pt"
DATA="corpus/WMTENDE/4pad"
#SRC_PATH="sockeye_autopilot/systems/wmt14_en_de/data/bpe/test.0.src"
SRC_PATH="sockeye_autopilot/systems/wmt14_en_de/data/bpe/dev.src"
#BEAM_SIZES=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35)
BEAM_SIZES=(5)
#TARGET_TRANSLATION="sockeye_autopilot/systems/wmt14_en_de/data/tst/test.0.trg"
TARGET_TRANSLATION="sockeye_autopilot/systems/wmt14_en_de/data/tst/dev.trg"
EPSILON_LIMITS=(4)
SRC_EPSILON_INJECTIONS=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15)
#SRC_EPSILON_INJECTIONS=(14 22)
START_PADS=(4)
LANGUAGE="de"
SAVE_DIR="output/"
FILE_NAME="translation_test.txt"

name=$(date +"%m-%d-%y")


for SRC_EPSILON_INJECTION in "${SRC_EPSILON_INJECTIONS[@]}"
do
    for BEAM_SIZE in "${BEAM_SIZES[@]}"
    do
        for START_PAD in "${START_PADS[@]}"
            do
                for EPSILON_LIMIT in "${EPSILON_LIMITS[@]}"
                do
                    file_name="${name}_beam_${BEAM_SIZE}_pads_${START_PAD}_epsilon_limit_${EPSILON_LIMIT}_spi_${SRC_EPSILON_INJECTION}.txt"
                    mkdir -p ${SAVE_DIR}

                    echo "Running evaluate for"
                    echo "  BEAM_SIZE=${BEAM_SIZE}"
                    echo "  START_PAD=${START_PAD}"
                    echo "  EPSILON_LIMIT=${EPSILON_LIMIT}"
                    echo "  SRC_EPSILON_INJECTIONS=${SRC_EPSILON_INJECTION}"

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

                    echo "Generated output for"
                    echo "  START_PADS=${START_PAD}"
                    echo "  BEAM_SIZE=${BEAM_SIZE}"
                    echo "  EPSILON_LIMIT=${EPSILON_LIMIT}"

                    echo "Stored results in ${SAVE_DIR}/${file_name}"
                    done
            done
    done
done



