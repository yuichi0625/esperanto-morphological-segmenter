import argparse
from typing import Dict

from word_segmenter import x_notation


def read_file(path: str) -> Dict[str, str]:
    word2annot = {}
    with open(path, encoding='utf-8') as f:
        for row in f.read().strip().split('\n'):
            word, annot = [x_notation(r) for r in row.split('\t')[:2]]
            word2annot[word] = annot
    return word2annot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--answer_file', required=True,
                        help='text file containing correct annotations')
    parser.add_argument('-p', '--pred_file', required=True,
                        help='text file containing prediction results')
    parser.add_argument('-s', '--show_incorrect', action='store_true',
                        help='show incorrect results')
    args = parser.parse_args()

    word2answer = read_file(args.answer_file)
    word2pred = read_file(args.pred_file)

    num_correct = 0
    num_incorrect = 0
    word_answer_pred = []
    for word, pred in word2pred.items():
        answer = word2answer.get(word)

        if answer is not None:
            if pred == answer:
                num_correct += 1
            else:
                num_incorrect += 1
                word_answer_pred.append([word, answer, pred])

    acc = num_correct / (num_correct + num_incorrect)

    print(f'accuracy        : {acc * 100:.2f} %')
    print(f'num of correct  : {num_correct} pcs')
    print(f'num of incorrect: {num_incorrect} pcs')

    if args.show_incorrect:
        for word, answer, pred in word_answer_pred:
            print(f'  {word}')
            print(f'    answer: {answer}')
            print(f'    pred  : {pred}')


if __name__ == '__main__':
    main()
