SCRIPTS_DIR=`dirname "$0"`
BASE_DIR=${SCRIPTS_DIR}/..

source ${SCRIPTS_DIR}/config.sh

# Combine the source and target training data into one file
#paste -d ' ||| ' train.shuf.src - - - - train.shuf.trg < /dev/null > combined_srctrg

# There are sentence pairs where either side is empty
# This will lead to fast align not being able to work propery, hence, remove these lines:
#cp combined_srctrg combined_srctrg_clean
#sed -i '/^ |||/d' combined_srctrg_clean
#sed -i '/ ||| $/d' combined_srctrg_clean


# Use fast_align to find the aligments of the training sentence pairs
alias fast_align=${TOOLS_DIR}/fast_align/fast_align
echo which fast_align
#fast_align -i ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/combined_srctrg_clean -d -o -v > forward.align_ende

# Run our script for making the training data Eager Feasible:
# Because add_epsilon performs in-place operations, we first create a copy
#cp forward.align_ende forward.align_ende.bkp
#python add_epsilons.py --align forward.align_ende --trg ${DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe/


