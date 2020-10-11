import argparse
import json
from collections import defaultdict
from pathlib import Path

from segmenter.const import WORD_BEGIN, WORD_END


def create_state_counts(sets_dir):
    """Count morphemems in each state(type)

    Args:
        sets_dir (str/pathlib.Path): "sets" directory path

    Returns:
        dict[str, int]: {state: number of morphemes in the state}
    """
    state_counts = {}
    for path in Path(sets_dir).glob('*.txt'):
        with open(path, encoding='utf-8') as f:
            state_counts[path.stem] = len(f.readlines())
    return state_counts


def create_transitions(paths, n, state_counts):
    """Make transition summary {prev_state: {next_state: probability}}

    Probability is calculated by
    frequency / sum of frequencies from the prev_state to all the next_states / number of morphemes in the next_state

    Args:
        paths (list[str]): List of train data paths
        n (int): number of n_gram
        state_counts (dict[str, int]): {state: number of morphemes in the state}

    Returns:
        dict[str, dict[str, float]]: {prev_state: {next_state: probability}}
    """
    # Check the given paths exist
    paths = [Path(path) for path in paths]
    for path in paths:
        assert path.exists(), f'{path} does not exist.'

    # Create a dictionary of {prev_state: {next_state: frequency}}
    # where "frequency" means how many times this prev-next state pair occurs in the train data
    transitions = defaultdict(lambda: defaultdict(float))
    for path in paths:
        with open(path, encoding='utf-8') as f:
            for row in f.read().splitlines():
                *_, segment, freq = row.split('\t')
                segment = [WORD_BEGIN, *segment.split('\''), WORD_END]

                for idx in range(len(segment) - n + 1):
                    # prev_state is converted to string because it's unable to save tuple key as json
                    prev_state = str(tuple(segment[idx:idx+n-1]))
                    next_state = segment[idx+n-1]
                    transitions[prev_state][next_state] += float(freq)

    # Convert the dictionary to {prev_state: {next_state: probability}}
    transition_probs = {}
    for prev_state in transitions.keys():
        transition_probs[prev_state] = {}
        for next_state, freq in transitions[prev_state].items():
            # state_counts does not include <EOS>
            state_count = state_counts.get(next_state, sum(state_counts.values()))
            transition_probs[prev_state][next_state] = freq / sum(transitions[prev_state].values()) / state_count

    return transition_probs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train_data', nargs='+',
                        default=['./EsperantoWordSegmenter/experiments/train.txt'],
                        help='indicate file paths for training')
    parser.add_argument('-n', '--n_gram', type=int, default=2,
                        help='set number of n_gram')
    parser.add_argument('-o', '--output_dir', default='markov_model',
                        help='indicate output directory')
    parser.add_argument('--ews_dir', default='./EsperantoWordSegmenter',
                        help='indicate the directory path to EsperantoWordSegmenter')
    args = parser.parse_args()

    sets_dir = Path(args.ews_dir) / 'morphemesByType' / 'sets'
    state_counts = create_state_counts(sets_dir)

    transitions = create_transitions(
        paths=args.train_data, n=args.n_gram, state_counts=state_counts)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / f'{args.n_gram}_gram_markov_model.json', 'w') as f:
        json.dump(transitions, f)


if __name__ == '__main__':
    main()
