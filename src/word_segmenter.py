from __future__ import annotations

import argparse
import enum
import os
from typing import Dict, List, Optional, Set, Tuple

from tqdm import tqdm  # type: ignore

# in Python, "enum.Enum" cannot have mutable variables
ignore_rules = False
word_counts: Dict[MarkovMorphemeType, int] = {}
total = 0


class RuleMorphemeType(enum.Enum):
    """
    Frist pass morpheme types
    For optional rule-based step
    """
    Standalone = enum.auto()
    Pronoun = enum.auto()
    Normal = enum.auto()
    WordEnd = enum.auto()
    Table = enum.auto()
    Article = enum.auto()
    TablePronounEnding = enum.auto()

    @classmethod
    def is_valid_ending(cls, value: Optional[RuleMorphemeType]) -> bool:
        return ignore_rules or (value is not None and value != cls.Normal)

    @classmethod
    def agrees_with_previous(cls, value: Optional[RuleMorphemeType], prev: Optional[RuleMorphemeType]) -> bool:
        if value == cls.TablePronounEnding:
            return ignore_rules or (prev == cls.Table or prev == cls.Pronoun)
        elif value == cls.Article:
            return ignore_rules or prev is None
        else:
            return ignore_rules or prev != cls.Article


def please_ignore_rules() -> None:
    global ignore_rules
    ignore_rules = True


def total_morphemes() -> int:
    global total
    if total == 0:
        total = sum(word_counts.values())
    return total


class MarkovMorphemeType(enum.Enum):
    """
    Second pass morpheme types
    For n-gram Markov disambiguation
    """
    AdjEnding = enum.auto()
    Adj = enum.auto()
    AdjSuffix = enum.auto()
    AdvEnding = enum.auto()
    Adverb = enum.auto()
    Adv = enum.auto()
    Article = enum.auto()
    Conjunction = enum.auto()
    Expression = enum.auto()
    MidEnding = enum.auto()
    NounEnding = enum.auto()
    NounHumanPrefix = enum.auto()
    NounHuman = enum.auto()
    NounHumanSuffix = enum.auto()
    NounPrefix = enum.auto()
    Noun = enum.auto()
    NounSuffix = enum.auto()
    Number = enum.auto()
    NumberSuffix = enum.auto()
    O = enum.auto()
    Preposition = enum.auto()
    PrepPrefix = enum.auto()
    Pronoun = enum.auto()
    TablePronounEnding = enum.auto()
    Table = enum.auto()
    TenseSuffix = enum.auto()
    VerbEnding = enum.auto()
    VerbPrefix = enum.auto()
    Verb = enum.auto()
    VerbSuffix = enum.auto()
    Start = enum.auto()
    End = enum.auto()

    def set_word_count(key: MarkovMorphemeType, value: int) -> None:
        global word_counts, total
        word_counts[key] = value
        total = 0

    def type_count(value: MarkovMorphemeType) -> int:
        if value in word_counts:
            return word_counts[value]
        else:
            return total_morphemes()

    @classmethod
    def to_rule_morpheme_type(cls, value: MarkovMorphemeType):
        to_word_end = {cls.AdjEnding, cls.AdvEnding, cls.NounEnding, cls.VerbEnding, cls.MidEnding, cls.O}
        to_table_pronoun_ending = {cls.TablePronounEnding}
        to_pronoun = {cls.Pronoun}
        to_article = {cls.Article}
        to_normal = {
            cls.Adj, cls.Adv, cls.NounHuman, cls.Noun, cls.Verb,
            cls.AdjSuffix, cls.NounHumanSuffix, cls.NounSuffix, cls.NumberSuffix, cls.TenseSuffix, cls.VerbSuffix,
            cls.NounHumanPrefix, cls.NounPrefix, cls.PrepPrefix, cls.VerbPrefix}
        to_standalone = {cls.Adverb, cls.Conjunction, cls.Expression, cls.Number, cls.Preposition}
        to_table = {cls.Table}
        to_none = {cls.Start, cls.End}

        if value in to_word_end:
            return RuleMorphemeType.WordEnd
        elif value in to_table_pronoun_ending:
            return RuleMorphemeType.TablePronounEnding
        elif value in to_pronoun:
            return RuleMorphemeType.Pronoun
        elif value in to_article:
            return RuleMorphemeType.Article
        elif value in to_normal:
            return RuleMorphemeType.Normal
        elif value in to_standalone:
            return RuleMorphemeType.Standalone
        elif value in to_table:
            return RuleMorphemeType.Table
        elif value in to_none:
            return None


class MarkovModel:
    """
    n-gram Markov Model
    """
    def __init__(self, filename: str, trie_root: TrieNode, n: int = 1):
        self.model_order = n
        self.transitions = self.make_transitions(filename)

    def make_transitions(self, filename: str):
        """
        Args:
            filename (str)
        Returns:
            dict[tuple[MarkovMorphemeType], dict[MarkovMorphemeType, float]]
        """
        multiplier = 0.00001

        individual_transitions = []
        with open(filename, encoding='utf-8') as f:
            name2type = {mt.name: mt for mt in MarkovMorphemeType}
            for line in f.read().strip().split('\n'):
                segmentation = [name2type[x[0].capitalize() + x[1:]] for x in line.split('\t')[2].split('\'')]
                freq = float(line.split('\t')[3])

                states = [MarkovMorphemeType.Start] * self.model_order + segmentation + [MarkovMorphemeType.End]

                for i in range(0, len(segmentation) + 1):
                    individual_transitions.append((states[i:i+self.model_order], states[i+self.model_order], freq))

        total_transitions: Dict[Tuple[MarkovMorphemeType, ...], Dict[MarkovMorphemeType, float]] = {}
        for transition in individual_transitions:
            key_, next_state, freq = transition
            key = tuple(key_)  # in Python, "list" cannot be a key of a "dict"
            if key not in total_transitions:
                total_transitions[key] = {}
            if next_state not in total_transitions[key]:
                total_transitions[key][next_state] = 0.0
            total_transitions[key][next_state] += freq

        totals = {k: sum(v.values()) for k, v in total_transitions.items()}
        transition_probabilities = {}
        for key in total_transitions.keys():
            for k, v in total_transitions[key].items():
                total_transitions[key][k] = v / totals[key] / float(MarkovMorphemeType.type_count(k)) * float(total_morphemes()) * multiplier
            transition_probabilities[key] = total_transitions[key]

        return transition_probabilities

    def evaluate_segmentation(self, segmentation: List[MarkovMorphemeType]) -> Tuple[float, int]:
        """
        Args:
            segmentation (list[MarkovMorphemeType])
        Returns:
            float, int
        """
        prev_states = [MarkovMorphemeType.Start] * self.model_order

        zero_penalty = 0
        score = 1.0
        for morph_type in segmentation + [MarkovMorphemeType.End]:
            if tuple(prev_states) in self.transitions and morph_type in self.transitions[tuple(prev_states)]:
                score *= self.transitions[tuple(prev_states)][morph_type]
            else:
                score = 0
                zero_penalty -= 1
            prev_states = prev_states[1:len(prev_states)] + [morph_type]

        return score, zero_penalty


class TrieNode:
    """
    Trie data structure for storing morphemes along with their types
    """
    def __init__(self, the_letter: str, the_root: Optional[TrieNode] = None) -> None:
        self.root = self if the_root is None else the_root
        self.letter = the_letter
        self.markov_morpheme_types: Set[MarkovMorphemeType] = set()
        self.rule_morpheme_types: Set[Optional[RuleMorphemeType]] = set()
        self.children: Dict[str, TrieNode] = dict()

    def get_or_add_child(self, the_letter: str, mt: Optional[MarkovMorphemeType] = None) -> TrieNode:
        """Add child if doesn't exist
           Add mt and smt (if not None) to the child's types
        """
        if the_letter in self.children:
            child = self.children[the_letter]
        else:
            new_node = TrieNode(the_letter, self.root)
            self.children[the_letter] = new_node
            child = new_node

        if mt is not None:
            child.markov_morpheme_types.add(mt)
            child.rule_morpheme_types.add(MarkovMorphemeType.to_rule_morpheme_type(mt))

        return child

    def add_word(self, mt: MarkovMorphemeType, word: str, index: int = 0) -> None:
        """Define new word in trie
        """
        if len(word) > index:
            letter = word[index]
            new_index = index + 1
            current_mt = mt if len(word) == new_index else None
            child = self.get_or_add_child(letter, current_mt)
            child.add_word(mt, word, new_index)

    def find_morphemes(self, word: str, start_index: int = 0, next_index: int = 0,
                       prev: Optional[RuleMorphemeType] = None) -> List[List[str]]:
        """First pass segmentation: look for all legal morphemes
        """
        solutions = list()
        valid_morphemes = {mt for mt in self.rule_morpheme_types
                           if RuleMorphemeType.agrees_with_previous(mt, prev)}

        # end of word
        if next_index == len(word):
            # makes valid morpheme
            if any([RuleMorphemeType.is_valid_ending(mt) for mt in valid_morphemes]):
                solutions.append([word[start_index:next_index]])

        # not the end of word
        else:
            # can start back at trie root
            for prev_morpheme in valid_morphemes:
                for lst in self.root.find_morphemes(word, next_index, next_index, prev_morpheme):
                    solutions.append([word[start_index:next_index]] + lst)

            # can go on with current path
            if word[next_index] in self.children:
                for sol in self.children[word[next_index]].find_morphemes(word, start_index, next_index + 1, prev):
                    solutions.append(sol)

        return solutions

    def get_all_tags(self, solution: List[str]) -> List[List[MarkovMorphemeType]]:
        if not solution:
            return [[]]
        else:
            next_solutions = self.get_all_tags(solution[1:len(solution)])
            return [[value] + sub_solution
                    for value in self.get_indexed_node(solution[0]).markov_morpheme_types
                    for sub_solution in next_solutions]

    def get_indexed_node(self, word: str, index: int = 0):
        """Find trie node representing word
        """
        if index >= len(word):
            return self
        elif word[index] in self.children:
            return self.children[word[index]].get_indexed_node(word, index + 1)
        else:
            return None


def build_trie(morphemes_by_type_dir: str) -> TrieNode:
    morpheme_type_file_names = {
        MarkovMorphemeType.AdjEnding: 'adjEnding.txt',
        MarkovMorphemeType.Adj: 'adj.txt',
        MarkovMorphemeType.AdjSuffix: 'adjSuffix.txt',
        MarkovMorphemeType.AdvEnding: 'advEnding.txt',
        MarkovMorphemeType.Adverb: 'adverb.txt',
        MarkovMorphemeType.Adv: 'adv.txt',
        MarkovMorphemeType.Article: 'article.txt',
        MarkovMorphemeType.Conjunction: 'conjunction.txt',
        MarkovMorphemeType.Expression: 'expression.txt',
        MarkovMorphemeType.MidEnding: 'midEnding.txt',
        MarkovMorphemeType.NounEnding: 'nounEnding.txt',
        MarkovMorphemeType.NounHumanPrefix: 'nounHumanPrefix.txt',
        MarkovMorphemeType.NounHuman: 'nounHuman.txt',
        MarkovMorphemeType.NounHumanSuffix: 'nounHumanSuffix.txt',
        MarkovMorphemeType.NounPrefix: 'nounPrefix.txt',
        MarkovMorphemeType.Noun: 'noun.txt',
        MarkovMorphemeType.NounSuffix: 'nounSuffix.txt',
        MarkovMorphemeType.Number: 'number.txt',
        MarkovMorphemeType.NumberSuffix: 'numberSuffix.txt',
        MarkovMorphemeType.O: 'o.txt',
        MarkovMorphemeType.Preposition: 'preposition.txt',
        MarkovMorphemeType.PrepPrefix: 'prepPrefix.txt',
        MarkovMorphemeType.Pronoun: 'pronoun.txt',
        MarkovMorphemeType.TablePronounEnding: 'tablePronounEnding.txt',
        MarkovMorphemeType.Table: 'table.txt',
        MarkovMorphemeType.TenseSuffix: 'tenseSuffix.txt',
        MarkovMorphemeType.VerbEnding: 'verbEnding.txt',
        MarkovMorphemeType.VerbPrefix: 'verbPrefix.txt',
        MarkovMorphemeType.Verb: 'verb.txt',
        MarkovMorphemeType.VerbSuffix: 'verbSuffix.txt'}

    trie_root = TrieNode('^')

    for key, val in morpheme_type_file_names.items():
        with open(os.path.join(morphemes_by_type_dir, val), encoding='utf-8') as f:
            words = f.read().strip().split('\n')
        for word in words:
            trie_root.add_word(key, word)
        MarkovMorphemeType.set_word_count(key, len(words))

    return trie_root


def solution_string(solutions: List[List[str]]) -> str:
    """for printing solution
    """
    return '\t'.join(['\''.join(lst) for lst in solutions])


def x_notation(word: str) -> str:
    """convert to x notation ("sxajnas")
    """
    hat_map = {
        'ĉ': 'cx',
        'ĝ': 'gx',
        'ĥ': 'hx',
        'ĵ': 'jx',
        'ŝ': 'sx',
        'ŭ': 'ux'}

    new_word = word
    for k, v in hat_map.items():
        new_word = new_word.replace(k, v)

    return new_word


def maximal_match(segmentations: List[List[str]]) -> List[str]:
    segs = set(tuple(seg) for seg in segmentations)  # in Python, "set" cannot include "list"
    scores = [(len(solution), solution) for solution in segs]
    if not scores:
        return []
    else:
        best = max(scores)
        return list(best[1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('-o', '--output_file', default='output.txt')
    parser.add_argument('-m', '--max_match', action='store_true',
                        help='Use maximal morpheme matching instead of Markov model')
    parser.add_argument('-r', '--random', action='store_true',
                        help='Skip disambiguation (step 2)')
    parser.add_argument('-n', '--no_rules', action='store_true',
                        help='Apply no rules in step 1')
    parser.add_argument('-b', '--use_bigram', action='store_true',
                        help='Use bigram Markov model')
    parser.add_argument('-t', '--use_trigram', action='store_true',
                        help='Use trigram Markov model')
    parser.add_argument('-tf', '--training_file',
                        default='../EsperantoWordSegmenter/experiments/train.txt')
    parser.add_argument('-mbtd', '--morphemes_by_type_directory',
                        default='../EsperantoWordSegmenter/morphemesByType/sets/')
    args = parser.parse_args()

    max_match = args.max_match
    random = args.random
    no_rules = args.no_rules
    use_bigram = args.use_bigram
    use_trigram = args.use_trigram

    if no_rules:
        please_ignore_rules()

    trie_root = build_trie(args.morphemes_by_type_directory)
    markov_model_order = 3 if use_trigram else 2 if use_bigram else 1
    markov_model = MarkovModel(args.training_file, trie_root, markov_model_order)

    with open(args.output_file, 'w', encoding='utf-8') as out:
        with open(args.input_file, encoding='utf-8') as f:
            for line in tqdm(f.read().strip().split('\n')):
                word = line.split('\t')[0].lower()

                # find legal segmentations
                solutions = trie_root.find_morphemes(x_notation(word))

                if random:
                    out.write(f'{solution_string(solutions)}\n')
                elif max_match:
                    out.write(f'{word}\t{solution_string([maximal_match(solutions)])}\n')
                else:
                    # Markov model
                    solution_scores = [
                        (solution, tag, markov_model.evaluate_segmentation(tag))
                        for solution in solutions
                        for tag in trie_root.get_all_tags(solution)]

                    best_solutions: List[List[str]] = []
                    best_so_far = (-1.0, 0)
                    for sol_and_score in solution_scores:
                        solution, _, score_penalty = sol_and_score
                        if best_so_far <= score_penalty:
                            if best_so_far < score_penalty:
                                best_so_far = score_penalty
                                best_solutions = []
                            best_solutions.append(solution)

                    out.write(f'{word}\t{solution_string([maximal_match(best_solutions)])}\n')


if __name__ == '__main__':
    main()
