import argparse
from pathlib import Path

from segmenter import Segmenter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('word',
                        help='input word to be segmented')
    parser.add_argument('-m', '--markov_model_dir', default='./markov_model',
                        help='indicate directory path to markov_model')
    parser.add_argument('-n', '--n_gram', type=int, default=2,
                        help='set number of n_gram')
    parser.add_argument('--ews_dir', default='./EsperantoWordSegmenter',
                        help='indicate the directory path to EsperantoWordSegmenter')
    args = parser.parse_args()

    segmenter = Segmenter(
        markov_model_dir=args.markov_model_dir,
        n=args.n_gram,
        sets_dir=Path(args.ews_dir) / 'morphemesByType' / 'sets')

    segms, segm_states, scores = segmenter.segment_and_evaluate(args.word)

    for segm, segm_state, score in zip(segms, segm_states, scores):
        print(f'score: {score}, segm: {segm}, segm_state: {segm_state}')


if __name__ == '__main__':
    main()
