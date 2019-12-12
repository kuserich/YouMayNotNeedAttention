SCRIPTS_DIR=`dirname "$0"`
BASE_DIR=${SCRIPTS_DIR}/..

source ${SCRIPTS_DIR}/config.sh

export CUDA_VISIBLE_DEVICES=5


# Model and corpus of child model
#MODEL="exps-11-20-kd/20191122-163749/model208000.pt"
#MODEL="exps-11-20-kd/20191122-163749/model312000.pt"
#DATA="corpus/WMTENDE/11-20-kd"

# Model and corpus of base line Press & Smith Model
MODEL="exps-10-22/20191025-161111/model390000.pt"
DATA="data/10-25-align-eps/corpus"

# Model and corpus of base line Press & Smith model after 35 Epochs
#MODEL="exps-10-22/20191025-161111/model526500.pt"
#DATA="data/10-25-align-eps/corpus"

# Model and corpus of base line P&S model trained with partially incorrect training data
#MODEL="exps/model390000.pt"
#DATA="corpus/WMTENDE/4pad"

#MODEL="exps20190909-161036/model383500.pt"
#MODEL="exps20190909-161036/model13000.pt"
#MODEL="exps-10-30/20191030-214313/model13000.pt"
#MODEL="data/wmt14_en_de/bpe/exps/20191031-170132/model13000.pt"
#SRC_PATH="sockeye_autopilot/systems/wmt14_en_de/data/bpe/test.0.src"
#SRC_PATH="sockeye_autopilot/systems/wmt14_en_de/data/bpe/dev.src"
#SRC_PATH="/mnt/storage/scratch1/goeckeritz/dev.bpe.en"
SRC_PATH="/srv/scratch1/goeckeritz/dev.bpe.en"
#SRC_PATH="sockeye_autopilot/systems/wmt14_en_de/data/bpe-split-all/x990230"
#BEAM_SIZES=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35)
BEAM_SIZES=(16 17 18 19 20 21 22)
#TARGET_TRANSLATION="sockeye_autopilot/systems/wmt14_en_de/data/tst/test.0.trg"
TARGET_TRANSLATION="sockeye_autopilot/systems/wmt14_en_de/data/tst/dev.trg"
EPSILON_LIMITS=(3)
SRC_EPSILON_INJECTIONS=(4 9)
#SRC_EPSILON_INJECTIONS=(4)
START_PADS=(4)
LANGUAGE="de"
SAVE_DIR="output/default/"
FILE_NAME="translation_test.txt"
PREFIX="default_"
SUFFIX=""

if [[ -d $SRC_PATH ]]; then
    echo "Processing src dir";
    for entry in "$SRC_PATH"/*
    do
        PREFIX=$(basename $entry)
        file_name="${PREFIX}${name}_beam_5_pads_4_epsilon_limit_3_spi_9${SUFFIX}.txt"
        echo $file_name
        python model/generate.py \
          --checkpoint ${MODEL} \
          --data ${DATA} \
          --src_path ${entry} \
          --beam_size 5 \
          --epsilon_limit 3 \
          --src_epsilon_injection 9 \
          --start_pads 4 \
          --save_dir ${SAVE_DIR} \
          --file_name ${file_name}
    done
elif [[ -f $SRC_PATH ]]; then
    echo "processing file";
    name=$(date +"%m-%d-%y")
    for SRC_EPSILON_INJECTION in "${SRC_EPSILON_INJECTIONS[@]}"
    do
        for BEAM_SIZE in "${BEAM_SIZES[@]}"
        do
            for START_PAD in "${START_PADS[@]}"
                do
                    for EPSILON_LIMIT in "${EPSILON_LIMITS[@]}"
                    do
                        file_name="${PREFIX}${name}_beam_${BEAM_SIZE}_pads_${START_PAD}_epsilon_limit_${EPSILON_LIMIT}_spi_${SRC_EPSILON_INJECTION}${SUFFIX}.txt"
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

                        echo "Stored results in ${SAVE_DIR}${file_name}"
                        done
                done
        done
    done

else
    echo "$SRC_PATH is not valid"
    exit 1
fi
