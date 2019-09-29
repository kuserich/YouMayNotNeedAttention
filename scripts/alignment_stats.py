import sys
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
parser.add_argument(
    '--align', type=str,
    help="Location of the alignment data")
parser.add_argument(
    '--src', type=str,
    help="Location of the src data")
parser.add_argument(
    '--trg', type=str,
    help="Location of the training data")
parser.add_argument(
    "--output", type=str, default="output/stats.txt",
    help="Number of padding symbols to add to the beginning of the trg"
         " sentence.")
parser.add_argument(
    "--test", type=str2bool, nargs='?',
    const=True, default=False,
    help="Activate test mode")

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


def compute_stats_from_file(alignments_file):
    pair_distances = []
    line_distances = []
    total_distance = 0
    total_num_words = 0
    total_distance_eps_required = 0
    with open(alignments_file) as file:
        for line in file:
            line_distance = 0
            words = line.split()
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

    return (pair_distances, line_distances, total_distance, total_num_words)


def reduce_consecutive_tokens(aList):
    consecutive_tokens = []
    num_consecutive = 0
    x = 0
    for x in aList:
        if x == 1:
            num_consecutive += 1
        elif x == 0 and num_consecutive != 0:
            consecutive_tokens.append(num_consecutive)
            num_consecutive = 0
    if x != 0 and num_consecutive != 0:
        consecutive_tokens.append(num_consecutive)
        num_consecutive = 0
    return consecutive_tokens


def count_epsilon_tokens_in_file(file):
    TRG_EPSILON = '@@@@'
    SRC_EPSILON = '@@@'
    START_PAD = '@str@@'

    line_tokens = []
    consecutive_epsilon_tokens = []
    total_tokens = 0
    total_epsilon_tokens = 0
    total_padding_tokens = 0
    total_end_padding_tokens = 0

    with open(file) as f:
        for line in f:
            tokens = line.split()
            previous = None
            consecutive_tokens = []
            for token in tokens:
                if token == START_PAD:
                    total_padding_tokens += 1
                elif token == TRG_EPSILON or token == SRC_EPSILON:
                    total_epsilon_tokens += 1
                    if token == previous:
                        consecutive_tokens.append(1)
                    else:
                        consecutive_tokens.append(0)
                previous = token

            consecutive_epsilon_tokens.append(
                reduce_consecutive_tokens(consecutive_tokens))
            line_tokens.append(len(tokens))
            total_tokens += len(tokens)

    return (
        total_tokens, total_epsilon_tokens,
        total_padding_tokens, line_tokens, consecutive_epsilon_tokens
    )


def run(align, src, trg, output):
    pair_distances, line_distances, total_distance, total_num_words = compute_stats_from_file(align)
    average_pair_distance = reduce(sum, pair_distances) / len(pair_distances)
    average_line_distance = reduce(sum, line_distances) / len(line_distances)

    total_tokens_src, total_epsilon_tokens_src, total_padding_tokens_src, line_tokens_src, consecutive_epsilon_tokens_src = count_epsilon_tokens_in_file(src)

    average_tokens_per_line = reduce(sum, line_tokens_src) / len(line_tokens_src)

    total_tokens_trg, total_epsilon_tokens_trg, total_padding_tokens_trg, line_tokens_trg, consecutive_epsilon_tokens_trg = count_epsilon_tokens_in_file(trg)

    message = (
        "ALIGNMENT STATISTICS",
        "=========================",
        "Number of Lines: %d" % len(line_distances),
        "Number of Words: %d" % total_num_words,
        "Total Distance: %d" % total_distance,
        "Average Pair Distance: %d" % average_pair_distance,
        "Average Line Distance: %d" % average_line_distance,
        "",
        "EPSILON STATISTICS (SRC)",
        "=========================",
        "Number of Tokens: %d" % total_tokens_src,
        "Number of Epsilon Tokens: %d" % total_epsilon_tokens_src,
        "Number of Padding Tokens: %d" % total_padding_tokens_src,
        "",
        "EPSILON STATISTICS (TRG)",
        "=========================",
        "Number of Tokens: %d" % total_tokens_trg,
        "Number of Epsilon Tokens: %d" % total_epsilon_tokens_trg,
        "Number of Padding Tokens: %d" % total_padding_tokens_trg,
    )

    print("")
    for entry in message:
        print(entry)
    print("")


# TESTS

def _test__reduce_consecutive_tokens():
    test_cases = [
        {
            "desc": "List starting with single 0 and consecutive 1s",
            "input": [0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1],
            "expected": [3, 2, 1, 1]
        },
        {
            "desc": "List starting with single 0 and ending with consecutive 1s",
            "input": [0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1],
            "expected": [3, 2, 1, 3]
        },
        {
            "desc": "Consecutive 0s",
            "input": [
                0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0,
                1, 1, 1, 0, 0, 0],
            "expected": [3, 2, 1, 3]
        },
        {
            "desc": "Only 0s",
            "input": [0, 0, 0, 0, 0, 0, 0, 0, 0],
            "expected": []
        },
        {
            "desc": "Only 1s",
            "input": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            "expected": [10]
        },
        {
            "desc": "Empty list",
            "input": [],
            "expected": []
        },
    ]

    for case in test_cases:
        input = case["input"]
        desc = case["desc"]
        expected = case["expected"]
        actual = reduce_consecutive_tokens(input)

        if expected != actual:
            print("Test failed: "+desc)
            print("Input: ", input)
            print("Expected:", expected)
            print("Actual: ", actual)


def test():
    _test__reduce_consecutive_tokens()


if (args.test):
    print("Running tests")
    test()
else:
    run(args.align, args.src, args.trg, args.output)
