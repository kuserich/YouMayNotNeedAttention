import argparse
import json
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
    '--src', type=str,
    help="Location of the src data")
parser.add_argument(
    "--save", type=str2bool, nargs='?',
    const=True, default=False,
    help="Save results")
parser.add_argument(
    "--test", type=str2bool, nargs='?',
    const=True, default=False,
    help="Activate test mode")

args = parser.parse_args()


def sum(a, b):
    """Return the sum of two numbers"""
    return a + b


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
    line_epsilon_tokens = []
    consecutive_epsilon_tokens = []
    total_tokens = 0
    total_epsilon_tokens = 0
    total_padding_tokens = 0
    total_end_padding_tokens = 0
    line_end_padding_tokens = []

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


            # if there is at least one padding token, assuming last token = EOS
            if tokens[-2] == TRG_EPSILON or tokens[-2] == SRC_EPSILON:
                num_end_padding_tokens = 0
                for i in range(len(tokens) - 2, 0, -1):
                    if tokens[i] == TRG_EPSILON or tokens[i] == SRC_EPSILON:
                        num_end_padding_tokens += 1
                    else:
                        break
                total_end_padding_tokens += num_end_padding_tokens
                line_end_padding_tokens.append(num_end_padding_tokens)


            consecutive_epsilon_tokens.append(
                reduce_consecutive_tokens(consecutive_tokens))
            line_tokens.append(len(tokens))
            line_epsilon_tokens.append(len(token))
            total_tokens += len(tokens)

    return (
        total_tokens, total_epsilon_tokens,
        total_padding_tokens, line_tokens, consecutive_epsilon_tokens,
        line_epsilon_tokens, total_end_padding_tokens, line_end_padding_tokens
    )


def sum(a, b):
    """Return the sum of two numbers"""
    return a + b


def count_tokens(line):
    """

    Every epsilon token in a <i>source</i> sentence is a padding token.

    :param file:
    :return:
    """
    EOS = '<eos>'
    TRG_EPSILON = '@@@@'
    SRC_EPSILON = '@@@'
    START_PAD = '@str@@'

    tokens = line.split()

    num_total = len(tokens)
    num_trg = 0
    num_src = 0
    num_pad = 0

    for token in tokens:
        if token == TRG_EPSILON:
            num_trg += 1
        elif token == SRC_EPSILON:
            num_src += 1
        elif token == START_PAD:
            num_pad += 1

    # previous = None
    # first = None
    # for token in reversed(tokens):
    #     if not first:
    #         first = token
    #         previous = token
    #         continue

    return (num_total, num_trg, num_src, num_pad)

def run(src, save=False):
    current_index = 0
    with open(src, "r") as file:
        lines = file.readlines()

        with open(src + ".epstats", "w") as outfile:
            outfile.write("total,trg,src,start_pad\n")
            for line in lines:
                num_total, num_trg, num_src, num_pad = count_tokens(line)
                outfile.write(','.join(map(str, [current_index, num_total, num_trg, num_src, num_pad])) + "\n")
                current_index += 1

def run_old(src, save=False):
    total_tokens, total_epsilon_tokens, total_padding_tokens, line_tokens, consecutive_epsilon_tokens, line_epsilon_tokens, total_end_padding_tokens, line_end_padding_tokens = count_epsilon_tokens_in_file(src)

    average_end_padding_tokens = reduce(sum, line_end_padding_tokens) / len(line_end_padding_tokens)
    average_line_length = reduce(sum, line_tokens) / len(line_tokens)
    average_line_epsilon_tokens = reduce(sum, line_epsilon_tokens) / len(line_epsilon_tokens)

    message = (
        "EPSILON STATISTICS",
        "=========================",
        "Number of Lines: %d" % len(line_tokens),
        "Number of Tokens: %d" % total_tokens,
        "Number of Epsilon Tokens: %d" % total_epsilon_tokens,
        "Number of Padding Tokens: %d" % total_padding_tokens,
        "Number of End Padding Tokens: %d" % total_end_padding_tokens,
        "Average Number of Tokens per line: {d:.3f}".format(d=average_line_length),
        "Average Number of Epsilon Tokens per line: {d:.3f}".format(d=average_line_epsilon_tokens),
        "Average Number of End Epsilon Tokens per line: {d:.5f}".format(d=average_end_padding_tokens),
    )

    print("")
    for entry in message:
        print(entry)
    print("")

    if save:
        data = {
            "num_lines": len(line_tokens),
            "num_tokems": total_tokens,
            "num_epsilon_tokens": total_epsilon_tokens,
        }
        with open(src + ".epstats", "w") as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)


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
    run(args.src, save=args.save)
