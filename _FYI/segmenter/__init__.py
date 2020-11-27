from .markov_model import MarkovModel
from .word_segmenter import WordSegmenter


class Segmenter:
    """Segmenter for segmenting word into morphemes and evaluate possibilities of each group of segmented morphemes

    segmenter = Segmenter(markov_model_dir, n, sets_dir)
    segms, segm_states, scores = segmenter.segment(word)
    """
    def __init__(self, markov_model_dir, n, sets_dir='../EsperantoWordSegmenter/morphemesByType/sets'):
        """
        Args:
            model_dir (str/pathlib.Path): path to markov_model
            n (int): number of n_gram
            sets_dir (str): "sets" directory path
        """
        self.markov_model = MarkovModel(model_dir=markov_model_dir, n=n)
        self.word_segmenter = WordSegmenter(sets_dir=sets_dir)

    def segment_and_evaluate(self, word):
        """Segment word into morphemes and evaluate possible scores for each group of segmented morphemes

        Args:
            word (str): word to be segmented

        Returns:
            tuple: Tuple containing
                segms (list[list[str]]): Sorted list of list of morphems
                segm_states (list[list[str]]): Sorted list of list of state
                scores (list[float]): Sorted list of score
        """
        scores = []
        segms, segm_states = self.word_segmenter.segment(word)

        if segms:
            scores = self.markov_model.evaluate(segm_states)
            scores, segms, segm_states = [
                list(tuple_) for tuple_ in
                zip(*sorted(zip(scores, segms, segm_states), reverse=True))]

        return segms, segm_states, scores
