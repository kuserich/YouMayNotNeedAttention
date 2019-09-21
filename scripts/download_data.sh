SCRIPTS_DIR=`dirname "$0"`
BASE_DIR=${SCRIPTS_DIR}/..

source ${SCRIPTS_DIR}/config.sh

SOCKEYE_DATA_DIR=${DATA_DIR}/sockeye_autopilot

sockeye-autopilot --task ${LANGUAGE_DATA} --model none --workspace ${SOCKEYE_DATA_DIR}

cd ./${SOCKEYE_DATA_DIR}/systems/${LANGUAGE_DATA}/data/bpe
gunzip *
paste -d '|'  train.src train.trg | shuf | awk -v FS='|' '{ print $1 > "train.shuf.src" ; print $2 > "train.shuf.trg" }'
