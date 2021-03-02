from pathlib import Path
from typing import List

from src.word_segmenter import (
    build_trie, maximal_match, solution_string, x_notation, MarkovModel)


class EsperantoWordSegmenter:
    def __init__(self, ngram: int = 2) -> None:
        self.trie_root = build_trie(
            str(Path(__file__).parent / './EsperantoWordSegmenter/morphemesByType/sets'))

        self.markov_model = MarkovModel(
            str(Path(__file__).parent / './EsperantoWordSegmenter/experiments/train.txt'),
            self.trie_root,
            ngram if ngram in {1, 2, 3} else 2)

    def __call__(self, word: str) -> str:
        solutions = self.trie_root.find_morphemes(x_notation(word.lower()))

        solution_scores = [
            (solution, tag, self.markov_model.evaluate_segmentation(tag))
            for solution in solutions
            for tag in self.trie_root.get_all_tags(solution)]

        best_solutions: List[List[str]] = []
        best_so_far = (-1.0, 0)
        for sol_and_score in solution_scores:
            solution, _, score_penalty = sol_and_score
            if best_so_far <= score_penalty:
                if best_so_far < score_penalty:
                    best_so_far = score_penalty
                    best_solutions = []
                best_solutions.append(solution)

        solution = solution_string([maximal_match(best_solutions)])

        return self._restore(solution, word)

    def _restore(self, solution: str, word: str) -> str:
        i = 0
        restored = ''
        for letter in word:
            restored += letter

            if letter.lower() in {'ĉ', 'ĝ', 'ĥ', 'ĵ', 'ŝ', 'ŭ'}:
                i += 1

            if len(solution) - 1 > i and solution[i+1] == '\'':
                restored += '\''
                i += 1

            i += 1

        return restored
