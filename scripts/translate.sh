source ./scripts/config_translate_default.sh

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --gpu)
    CUDA_VISIBLE_DEVICES="$2"
    shift # past argument
    shift # past value
    ;;
    --model)
    MODEL="$2"
    shift # past argument
    shift # past value
    ;;
    --vocabulary)
    DATA="$2"
    shift # past argument
    shift # past value
    ;;
    --src)
    SRC_PATH="$2"
    shift # past argument
    shift # past value
    ;;
    --beam)
    BEAM_SIZES="$2"
    shift # past argument
    shift # past value
    ;;
    --trg)
    TARGET_TRANSLATION="$2"
    shift # past argument
    shift # past value
    ;;
    --limit)
    EPSILON_LIMITS="$2"
    shift # past argument
    shift # past value
    ;;
    --spi)
    SRC_EPSILON_INJECTIONS="$2"
    shift # past argument
    shift # past value
    ;;
    --pads)
    START_PADS="$2"
    shift # past argument
    shift # past value
    ;;
    --lang)
    LANGUAGE="$2"
    shift # past argument
    shift # past value
    ;;
    --outdir)
    SAVE_DIR="$2"
    shift # past argument
    shift # past value
    ;;
    --prefix)
    PREFIX="$2"
    shift # past argument
    shift # past value
    ;;
    --suffix)
    SUFFIX="$2"
    shift # past argument
    shift # past value
    ;;
    --class)
    MODEL_CLASS="$2"
    shift # past argument
    shift # past value
    ;;
    --outname)
    FILE_NAME="$2"
    shift # past argument
    shift # past value
    ;;
    --config)
    CONFIG="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters


if [ -z ${CONFIG+x} ];
    then
    echo "No config provided. Using default config.";
    else
    source ${CONFIG};
fi

echo "CUDA_VISIBLE_DEVICES    = ${CUDA_VISIBLE_DEVICES}"
echo "MODEL                   = ${MODEL}"
echo "CORPUS                  = ${CORPUS}"
echo "SRC_PATH                = ${SRC_PATH}"
echo "BEAM_SIZES              = ${BEAM_SIZES}"
echo "TARGET_TRANSLATION      = ${TARGET_TRANSLATION}"
echo "EPSILON_LIMITS          = ${EPSILON_LIMITS}"
echo "SRC_EPSILON_INJECTIONS  = ${SRC_EPSILON_INJECTIONS}"
echo "START_PADS              = ${START_PADS}"
echo "LANGUAGE                = ${LANGUAGE}"
echo "SAVE_DIR                = ${SAVE_DIR}"
echo "PREFIX                  = ${PREFIX}"
echo "SUFFIX                  = ${SUFFIX}"
echo "MODEL_CLASS             = ${MODEL_CLASS}"
echo "FILE_NAME               = ${FILE_NAME}"

if [[ -n $1 ]]; then
    echo "Last line of file specified as non-opt/last argument:"
    tail -1 "$1"
fi


export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES}



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
    current_date=$(date +"%m-%d-%y")
    for SRC_EPSILON_INJECTION in "${SRC_EPSILON_INJECTIONS[@]}"
    do
        for BEAM_SIZE in "${BEAM_SIZES[@]}"
        do
            for START_PAD in "${START_PADS[@]}"
                do
                    for EPSILON_LIMIT in "${EPSILON_LIMITS[@]}"
                    do
                        file_name="${PREFIX}"
                        file_name="${file_name}${MODEL_CLASS}"
                        file_name="${file_name}_beam_${BEAM_SIZE}"
                        file_name="${file_name}_pads_${START_PAD}"
                        file_name="${file_name}_epsilon_limit_${EPSILON_LIMIT}"
                        file_name="${file_name}_spi_${SRC_EPSILON_INJECTION}"
                        file_name="${file_name}_${current_date}"
                        file_name="${file_name}${SUFFIX}"
                        file_name="${file_name}.txt"

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