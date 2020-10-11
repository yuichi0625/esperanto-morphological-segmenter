from pathlib import Path

from .const import WORD_BEGIN, WORD_END
from .preprocess import apply_hatmap


class WordSegmenter:
    """Word segmenter for segmenting word into morphemes

    word_segmenter = WordSegmenter(sets_dir)
    segms, segm_states = word_segmenter.segment(word)
    """
    def __init__(self, sets_dir):
        """
        Args:
            sets_dir (str): "sets" directory path
        """
        self.state2morphemes = self.create_state2morphemes(sets_dir)
        self.normal_states = [
            'adj', 'adv', 'nounHuman', 'noun', 'verb',
            'adjSuffix', 'nounHumanSuffix', 'nounSuffix', 'numberSuffix', 'tenseSuffix', 'verbSuffix',
            'nounHumanPrefix', 'nounPrefix', 'prepPrefix', 'verbPrefix']

    @staticmethod
    def create_state2morphemes(sets_dir):
        """Map each state(type) to all the morphemes in the state

        Args:
            sets_dir (str): "sets" directory path

        Returns:
            dict[str, set[str]]: {morpheme state: all the morphemes in the given state}
        """
        def load_text_file(path):
            with open(path, encoding='utf-8') as f:
                text = apply_hatmap(f.read())
                return set(text.splitlines())

        state2morphemes = {}
        for path in Path(sets_dir).glob('*.txt'):
            state2morphemes[path.stem] = load_text_file(path)

        return state2morphemes

    def segment(self, word):
        """Segment word into morphemes

        Extract all the possible segmentations,
        so the results can be more than 100 if the word is long and highly agglutinative

        Args:
            word (str): word to be segmented

        Returns:
            function: segment_recursively
        """
        # Convert alphabet + x to hatted alphabet
        word = apply_hatmap(word)

        def segment_recursively(start_idx, prev_state, segm, segm_state, segms, segm_states):
            """
            Args:
                start_idx (int): start index to slice word into morpheme
                prev_state (str): previous state
                segm (list[str]): List of morphemes
                segm_state (list[str]): List of states
                segms (list[list[str]]): List of list of morphems
                segm_states (list[list[str]]): List of list of states

            Returns:
                tuple: Tuple containing
                    segms (list[list[str]]): List of list of morphems
                    segm_states (list[list[str]]): List of list of state
            """
            # Word end has to be other than "normal states"
            if start_idx == len(word) and prev_state not in self.normal_states:
                segms.append(segm)
                segm_state.append(WORD_END)
                segm_states.append(segm_state)

            # "Article" is alone, so nothing follows it
            elif prev_state != 'article':
                for idx in range(start_idx + 1, len(word) + 1):
                    morpheme = word[start_idx:idx]
                    for curr_state, morphemes in self.state2morphemes.items():
                        if morpheme.lower() in morphemes:
                            # "TablePronounEnding" has to follow either "table" or "pronoun"
                            if curr_state == 'tablePronounEnding' and prev_state not in {'table', 'pronoun'}:
                                continue
                            # "Article" is alone, so only "<BOW>" can be followed by it
                            if curr_state == 'article' and prev_state != WORD_BEGIN:
                                continue
                            segm_ = segm.copy()
                            segm_.append(morpheme)
                            segm_state_ = segm_state.copy()
                            segm_state_.append(curr_state)
                            segms, segm_states = segment_recursively(
                                idx, curr_state, segm_, segm_state_, segms, segm_states)
            return segms, segm_states

        return segment_recursively(
            start_idx=0, prev_state=WORD_BEGIN, segm=[], segm_state=[WORD_BEGIN], segms=[], segm_states=[])
