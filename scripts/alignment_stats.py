import argparse
from functools import reduce


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(
    description="Compute alignment statistics and count number of epsilon"
                " tokens in source and target.")
parser.add_argument('--align', type=str, help="Location of the alignment data")

args = parser.parse_args()


def split_fast_align_pair(aStr):
    """Split an alignment pair in a line of alignments of fast_align into
    two numbers
    """
    parts = aStr.split('-')
    return (int(parts[0], 10), int(parts[1], 10))


def sum(a, b):
    """Return the sum of two numbers"""
    return a + b

def compute_epsilon_distance(line):
    epsilon_distance = 0
    for pair_str in line.split():
        i, j = split_fast_align_pair(pair_str)
        residual_distance = i - j - epsilon_distance
        if residual_distance > 0:
            epsilon_distance += residual_distance
    return epsilon_distance

def compute_stats_from_file(alignments_file):
    pair_distances = []
    line_distances = []
    total_distance = 0
    total_num_words = 0
    total_distance_eps_required = 0
    line_epsilon_distances = []
    total_epsilon_distance = 0
    with open(alignments_file) as file:
        for line in file:
            line_distance = 0
            words = line.split()
            epsilon_distance = compute_epsilon_distance(line)
            line_epsilon_distances.append(epsilon_distance)
            total_epsilon_distance += epsilon_distance
            for pair in words:
                i, j = split_fast_align_pair(pair)
                distance = i - j
                distance_abs = abs(distance)
                line_distance += distance_abs
                total_distance += distance_abs
                pair_distances.append(distance_abs)

                if distance > 0:
                    total_distance_eps_required += distance

            line_distances.append(line_distance)
            total_num_words += len(words)

    return (pair_distances, line_distances, total_distance, total_num_words, line_epsilon_distances, total_epsilon_distance)


def run(align):
    pair_distances, line_distances, total_distance, total_num_words, line_epsilon_distances, total_epsilon_distance = compute_stats_from_file(align)
    average_pair_distance = reduce(sum, pair_distances) / len(pair_distances)
    average_line_distance = reduce(sum, line_distances) / len(line_distances)
    average_line_epsilon_distance = reduce(sum, line_epsilon_distances) / len(line_epsilon_distances)

    message = (
        "ALIGNMENT STATISTICS",
        "=========================",
        "Number of Lines: %d" % len(line_distances),
        "Number of Words: %d" % total_num_words,
        "Total Distance: %d" % total_distance,
        "Average Pair Distance: %d" % average_pair_distance,
        "Average Line Distance: %d" % average_line_distance,
        "Total Epsilon Distance: %d" % total_epsilon_distance,
        "Average Line Epsilon Distance: %d" % average_line_epsilon_distance,
    )

    print("")
    for entry in message:
        print(entry)
    print("")


if not args.align:
    print("Error: Please provide alignments file")
    exit()

run(args.align)