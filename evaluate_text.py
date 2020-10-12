import argparse
import csv
from pathlib import Path

from segmenter import Segmenter
from segmenter.preprocess import apply_hatmap


def load_eval_data(path):
    """Load text data and return generator for each row

    Each row of given text data is assumed to be "word(tab)word segmented by apostrophe"

    Args:
        paths (list[str/pathlib.Path]): list of eval data path

    Yields:
        tuple: Tuple containing:
            word (str): word
            segment (list[str]): list of segmented morphemes from word
    """
    path = Path(path)
    assert path.exists(), f'{path} does not exist.'

    with open(path, encoding='utf-8') as f:
        for row in f.read().splitlines():
            word, segm_word = [apply_hatmap(word) for word in row.split('\t')[:2]]
            segment = segm_word.split('\'')
            yield word, segment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text_file',
                        default='./EsperantoWordSegmenter/experiments/test.txt',
                        help='indicate file paths for evaluating')
    parser.add_argument('-m', '--markov_model_dir', default='./markov_model',
                        help='indicate directory path to markov_model')
    parser.add_argument('-n', '--n_gram', type=int, default=2,
                        help='set number of n_gram')
    parser.add_argument('-o', '--output_path', default='output.csv',
                        help='indicate output csv file path')
    parser.add_argument('--ews_dir', default='./EsperantoWordSegmenter',
                        help='indicate the directory path to EsperantoWordSegmenter')
    args = parser.parse_args()

    segmenter = Segmenter(
        markov_model_dir=args.markov_model_dir,
        n=args.n_gram,
        sets_dir=Path(args.ews_dir) / 'morphemesByType' / 'sets')

    num_correct = 0
    num_incorrect = 0
    incorrect_results = []
    no_segmentation_results = []
    # There are the same words in consecutive rows in, for instance, train.txt and test.txt
    prev_word = ''
    for word, answer in load_eval_data(args.text_file):
        if word != prev_word:
            segms, _, _ = segmenter.segment_and_evaluate(word)
            # All the returned values are [] if no possible segmentations are found
            if segms:
                # Extract the most possible values
                segm = segms[0]
                if segm == answer:
                    num_correct += 1
                else:
                    num_incorrect += 1
                    incorrect_results.append([word, answer, segm])
            else:
                no_segmentation_results.append([word])
        prev_word = word

    # Save results as csv file
    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8-sig') as f:
        num_total = num_correct + num_incorrect
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows([['--- summary ---'], ['n_total', 'n_correct', 'n_incorrect', 'accuracy']])
        writer.writerow([num_total, num_correct, num_incorrect, num_correct / num_total])
        writer.writerows([[''], ['--- incorrect results ---'], ['word', 'answer', 'result']])
        writer.writerows(incorrect_results)
        writer.writerows([[''], ['--- no segmentation results ---']])
        writer.writerows(no_segmentation_results)


if __name__ == '__main__':
    main()
