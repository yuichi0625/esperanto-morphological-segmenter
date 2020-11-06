# Esperanto Morphological Segmenter
This is a reimplementation of [EsperantoWordSegmenter](https://github.com/tguinard/EsperantoWordSegmenter) in Python (originally in Scala), which is a tool for segmenting Esperanto words into morphemes.

This Python implementation has some modifications from the original one (for instance, training Markov Model is seperated from the main script).

The original paper is [here](https://ufal.mff.cuni.cz/pbml/105/art-guinard.pdf).

## Table of Contents
- [Requirements](#Requirements)
- [Installation](#Installation)
- [Usage](#Usage)
    - [train Markov Model](#train-Markov-Model)
    - [evaluate segmentation](#evaluate-segmentation)
- [Accuracy](#Accuracy)
- [Problems to be solved](#Problems-to-be-solved)

## Requirements
- Python >= 3.6

## Installation
```
git clone https://github.com/yuichi0625/reimplemented-esperanto-word-segmenter.git --recursive
```

## Usage
### train Markov Model
In the original implementation, every time you execute the main script, it loads train.txt and makes a trainsition map for n-gram Markov Model.  
In this reimplementation, I split this phase as a single script, which saves the transition map as a json file.  
**I already saved json files for bigram and trigram trained by train.txt, so you don't need to use this script if it's enough.**
```
usage: train_markov_model.py [-h] [-t TRAIN_DATA [TRAIN_DATA ...]] [-n N_GRAM]
                             [-o OUTPUT_DIR] [--ews_dir EWS_DIR]

optional arguments:
    -t, --train_data  indicate file paths for training
                      (default to "./EsperantoWordSegmenter/experiments/train.txt")
    -n, --n_gram      set number of n_gram
                      (default to 2)
    -o, --output_dir  indicate output directory
                      (default to "markov_model")
    --ews_dir         indicate the directory path to EsperantoWordSegmenter
                      (default to "./EsperantoWordSegmenter")
```

For instance,
```
python train_markov_model.py -t train1.txt train2.txt -n 3
```
Then it will save a json file containing a trainsition map for n-gram.

### evaluate segmentation
I made two scripts for evaluating the morphological segmenter.

1. For checking how a word will be segmented, use `evaluate_word.py`.
    ```
    usage: evaluate_word.py [-h] [-m MARKOV_MODEL_DIR] [-n N_GRAM]
                            [--ews_dir EWS_DIR] word

    positional arguments:
        word                    input word to be segmented

    optional arguments:
        -m, --markov_model_dir  indicate the directory path containing markov_model.json files
                                (default to "markov_model")
        -n, --n_gram            set number of n_gram
                                (default to 2)
        --ews_dir               indicate the directory path to EsperantoWordSegmenter
                                (default to "./EsperantoWordSegmenter")
    ```

    For instance,
    ```
    python evaluate_word.py hundo -n 2
    ```

    Then the output will be
    ```
    score: 2.6926387709385188e-12, segm: ['hund', 'o'], segm_state: ['<BOW>', 'nounHuman', 'nounEnding', '<EOW>']
    score: 9.657742579438868e-17,  segm: ['hun', 'do'], segm_state: ['<BOW>', 'adv', 'conjunction', '<EOW>']
    score: 1.8693218209110018e-17, segm: ['hun', 'do'], segm_state: ['<BOW>', 'adj', 'conjunction', '<EOW>']
    score: 3.629291807914485e-18,  segm: ['hun', 'do'], segm_state: ['<BOW>', 'noun', 'conjunction', '<EOW>']
    score: 0,                      segm: ['hund', 'o'], segm_state: ['<BOW>', 'nounHuman', 'o', '<EOW>']
    ```
    Where
    - `score`: possible score for each segmentation
    - `segm`: segmentation
    - `segm_state`: states (types) for the segmentation

1. For checking accuracy for a text file with annotations, use `evaluate_text.py`.  
    There are some text files with annotations in the directory `eval_data`.
    ```
    usage: evaluate_text.py [-h] [-t TEXT_FILE] [-m MARKOV_MODEL_DIR] [-n N_GRAM]
                            [-o OUTPUT_PATH] [--ews_dir EWS_DIR]

    optional arguments:
        -t, --text_file         input text file with annotations
                                (default to "./EsperantoWordSegmenter/experiments/test.txt")
        -m, --markov_model_dir  indicate the directory path containing markov_model.json files
                                (default to "markov_model")
        -n, --n_gram            set number of n_gram
                                (default to 2)
        -o, --output_path       indicate output csv file
                                (default to "output.csv")
        --ews_dir               indicate the directory path to EsperantoWordSegmenter
                                (default to "./EsperantoWordSegmenter")
    ```

    For instance,
    ```
    python evaluate_text.py -n 3 -o test.csv
    ```

    Then it outputs a csv file containing
    - `summary`: accuracy etc.
    - `incorrect results`: words that are segmented incorrectly
    - `no segmentation results`: words that the segmenter could not find any possible segmentation from

## Accuracy
| train data | evaluation data | n_gram | accuracy (%) | correct (pcs) | incorrect (pcs) |
| --- | --- | --- | --- | --- | --- |
| train.txt | test.txt | 2 | 97.51 | 10328 | 263 |
| train.txt | test.txt | 3 | 97.49 | 10326 | 265 |
| train.txt<br>test.txt | test.txt | 2 | 97.54 | 10331 | 260 |
| train.txt<br>test.txt | test.txt | 3 | 97.57 | 10334 | 257 |
| train.txt | random_words.txt | 2 | 75.0 | 12 | 4 |
| train.txt | random_words.txt | 3 | 81.25 | 13 | 3 |
| train.txt | liberafolio_2020_09_09.txt | 2 | 99.50 | 808 | 4 |
| train.txt | liberafolio_2020_09_09.txt | 3 | 99.50 | 808 | 4 |
| train.txt | liberafolio_2020_09_16.txt | 2 | 97.72 | 688 | 16 |
| train.txt | liberafolio_2020_09_16.txt | 3 | 97.72 | 688 | 16 |
| train.txt | liberafolio_2020_09_22.txt | 2 | 97.65 | 625 | 15 |
| train.txt | liberafolio_2020_09_22.txt | 3 | 97.81 | 626 | 14 |

## Problems to be solved
I met some problems when reimplementing the algorithm:

### Morphemes by Types
morphemesByType contains some confusing words, which interrupt prediction, e.g.  
1. "konat" (-> "kon" + "at")
1. "egoism" (-> "ego" + "ism")
1. "solist" (-> "sol" + "ist")
1. "nenio" (-> "neni" + "o")  
    Correlatives are ambiguous, because for instance "nenio" can be segmented into "neni" + "o", but "nenies" cannot.

### Dataset
The annotated train and test files include lots of falsely annotated words, e.g.  
- `Incorrect segmentation`:
    1. teknologio as teknolog'i'o (-> teknologi'o)
    1. faceti as fac'et'i (-> facet'i)
    1. finio as fi'ni'o (-> fini'o)
    1. decentraligo as de'centr'al'ig'o (-> de'central'ig'o)
- `Correct segmentation but incorrect tagging`:
    1. dis'kon'ig'o as adv'verb'noun'nounEnding (at least "ig" should be tagged as suffix)

### Markov Model
Some words are really difficult to segment, e.g.  
- `Both words exist`:
    1. farado as far'ad'o and farad'o
    1. esperanto as esper'ant'o and esperant'o
- `Syntactically correct but semantically incorrect`:
    1. katokulo as kat'o'kul'o (-> kat'okul'o)
    1. ledpretigisto as led'pret'i'gist'o (-> led'pret'ig'ist'o)
    1. edziĝoringo as edz'iĝ'or'ing'o (-> edz'iĝ'o'ring'o)
