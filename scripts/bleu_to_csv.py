import os
import sys
import json

directory = sys.argv[1]
csv_file = sys.argv[1]

with open(csv_file, "a") as csv:
    for file in os.listdir(directory):
        if file.endswith(".bleu"):
            with open(os.path.join(directory, file), "r") as bleu_file:
                data = json.loads(bleu_file.readline())

                # a file name usually looks like this:
                # 11-06-19_beam_5_pads_4_epsilon_limit_7_spi_24.txt.bleu
                # and we want beam, pads, epsilon and spi from it
                filename_split = file.split("_")

                beam = filename_split[2]
                start_pads = filename_split[4]
                epsilon_limit = filename_split[7]
                spi = filename_split[9].split(".")[0]

                print(beam, start_pads, epsilon_limit, spi, data["score"])

                csv.write(
                    "%d,%d,%d,%d,%d,%d" % (beam, start_pads, epsilon_limit, spi, data["score"], data["sys_len"])
                )