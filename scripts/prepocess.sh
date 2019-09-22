SCRIPTS_DIR=`dirname "$0"`
BASE_DIR=${SCRIPTS_DIR}/..

source ${SCRIPTS_DIR}/config.sh

# Combine the source and target training data into one file
paste -d ' ||| ' \
    ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/train.shuf.src \
    - - - - \
    ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/train.shuf.trg \
    < /dev/null \
    > ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/combined_srctrg;

# There are sentence pairs where either side is empty
# This will lead to fast align not being able to work propery, hence, remove these lines:
cp ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/combined_srctrg ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/combined_srctrg_clean
sed -i '/^ |||/d' ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/combined_srctrg_clean
sed -i '/ ||| $/d' ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/combined_srctrg_clean

# Use fast_align to find the aligments of the training sentence pairs
export OMP_NUM_THREADS=12
${TOOLS_DIR}/fast_align/fast_align -i ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/combined_srctrg_clean -d -o -v > forward.align_ende

# Run our script for making the training data Eager Feasible:
mkdir -p corpus/WMTENDE/4pad/
# Because add_epsilon performs in-place operations, we first create a copy
cp forward.align_ende forward.align_ende.bkp
python add_epsilons.py --align forward.align_ende \
    --trg ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/train.shuf.trg \
    --src ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/train.shuf.src \
    --left_pad 4 \
    --directory corpus/WMTENDE/4pad/
