SCRIPTS_DIR=`dirname "$0"`
BASE_DIR=${SCRIPTS_DIR}/..

source ${SCRIPTS_DIR}/config.sh

data_pairs=(
    "wmt14_de_en"
    "wmt14_fr_en"
    #"wmt14_en_de"
    "wmt14_en_fr"
    #wmt17_de_en,
    #wmt17_fi_en,
    #wmt17_lv_en,
    #wmt17_tr_en,
    #wmt17_en_de,
    #wmt17_en_fi,
    #wmt17_en_lv,
    #wmt17_en_tr,
    #wmt18_de_en,
    #wmt18_en_de
)

for i in "${data_pairs[@]}"
do
   : 
   sockeye-autopilot --task ${i} --model none --workspace ${DATA_DIR}
done