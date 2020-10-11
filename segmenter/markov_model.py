import json
import re
from functools import reduce
from operator import mul
from pathlib import Path


class MarkovModel:
    """N-gram Markov Model to evaluate which segmentations are more possible

    markov_model = MarkovModel(model_dir, n)
    scores = markov_model.evaluate(segm_states)
    """
    def __init__(self, model_dir, n):
        """
        Args:
            model_dir (str/pathlib.Path): path to markov_model
            n (int): number of n_gram
        """
        model_path = Path(model_dir) / f'{n}_gram_markov_model.json'
        self.transitions = self.load_model(model_path)
        self.n = n

    @staticmethod
    def load_model(path):
        """Load transition summary {prev_state(s): {next_state: probability}}

        Args:
            path (str/pathlib.Path): path to markov_model.json

        Returns:
            dict[str/tuple[str], dict[str, float]]: {prev_state(s): {next_state: probability}}
        """
        regex = re.compile(r'\'([<>\w]+)\'')

        with open(path, encoding='utf-8') as f:
            j = json.loads(f.read())

        transitions = {}
        for str_keys, kvp in j.items():
            keys = regex.findall(str_keys)
            if len(keys) == 1:
                transitions[keys[0]] = kvp
            else:
                transitions[tuple(keys)] = kvp

        return transitions

    def evaluate(self, states_list):
        """Calculate possible scores for each list of states

        Args:
            states_list (list[list[str]]): List of states (which is a list of state)

        Returns:
            list[float]: List of scores
        """
        scores = []
        for states in states_list:
            probs = []
            for idx in range(len(states) - self.n + 1):
                prev_state = states[idx:idx+self.n-1]
                prev_state = tuple(prev_state) if len(prev_state) > 1 else prev_state[0]
                next_state = states[idx+self.n-1]

                if self.transitions.get(prev_state) is None or self.transitions[prev_state].get(next_state) is None:
                    scores.append(0)
                    break
                else:
                    probs.append(self.transitions[prev_state][next_state])

            if len(probs) == (len(states) - self.n + 1):
                scores.append(self.calc_score(probs))

        return scores

    @staticmethod
    def calc_score(probs):
        """Calculate score

        Score is calculated by
        product of [alpha * probability | probability <- probabilities]

        Args:
            probs (list[float]): List of probabilities

        Returns:
            float: calculated score
        """
        # Originally alpha equals to number of total morphemes * 0.00001
        # which is roughly 0.13
        return reduce(mul, [0.13 * prob for prob in probs])
