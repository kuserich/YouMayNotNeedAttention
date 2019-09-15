SCRIPTS_DIR=`dirname "$0"`
BASE_DIR=${SCRIPTS_DIR}/..

source ${SCRIPTS_DIR}/config.sh

CHECKPOINT="model357500.pt"
DATA="corpus/WMTENDE/4pad"

python model/generate.py \
    --checkpoint exps/model357500.pt
    --data corpus/WMTENDE/4pad
    --src_path sockeye_autopilot/systems/wmt14_en_de/data/bpe/dev.src
    --beam_size 5
    --eval
    --target_translation sockeye_autopilot/systems/wmt14_en_de/data/tst/dev.trg
    --epsilon_limit 3
    --src_epsilon_injection 4
    --start_pads 5
    --language de
    --save_dir output/
