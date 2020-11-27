# Esperanto Morphological Segmenter
This is a reimplementation of [EsperantoWordSegmenter](https://github.com/tguinard/EsperantoWordSegmenter) in Python (originally in Scala), which is a tool for segmenting Esperanto words into morphemes.

The original paper is [here](https://ufal.mff.cuni.cz/pbml/105/art-guinard.pdf).

## Table of Contents
- [Requirements](#Requirements)
- [Installation](#Installation)
- [Usage](#Usage)
    - [src/word_segmenter.py](#srcword_segmenterpy)
    - [src/calc_accuracy.py](#srccalc_accuracypy)
- [Accuracy](#Accuracy)
- [Problems to be solved](#Problems-to-be-solved)

## Requirements
- Python >= 3.6
- tqdm

## Installation
```
git clone https://github.com/yuichi0625/reimplemented-esperanto-word-segmenter.git --recursive
```

## Usage
Please see [src/exec.bat]() / [src/exec.sh]() for more details.

### src/word_segmenter.py
This is the reimplementation of [WordSegmenter.scala]().
```
usage: word_segmenter.py [-h] [-o OUTPUT_FILE] [-m] [-r] [-n] [-b] [-t]
                         [-tf TRAINING_FILE]
                         [-mbtd MORPHEMES_BY_TYPE_DIRECTORY]
                         input_file

positional arguments:
  input_file

optional arguments:
  -o, --output_file
  -m, --max_match       Use maximal morpheme matching instead of Markov model
  -r, --random          Skip disambiguation (step 2)
  -n, --no_rules        Apply no rules in step 1
  -b, --use_bigram      Use bigram Markov model
  -t, --use_trigram     Use trigram Markov model
  -tf, --training_file
  -mbtd, --morphemes_by_type_directory
```

### src/calc_accuracy.py
This is a script for checking the accuracy between answer and prediction.
```
usage: calc_accuracy.py [-h] -a ANSWER_FILE -p PRED_FILE [-s]

optional arguments:
  -a, --answer_file     text file containing correct annotations
  -p, --pred_file       text file containing prediction results
  -s, --show_incorrect  show incorrect results
```

## Accuracy
| train data | evaluation data | n_gram | accuracy (%) | correct (pcs) | incorrect (pcs) |
| --- | --- | --- | --- | --- | --- |
| train.txt | test.txt | 2 | 97.74 | 10352 | 239 |
| train.txt | test.txt | 3 | 97.81 | 10359 | 232 |
| train.txt | random_words.txt | 2 | 87.5 | 14 | 2 |
| train.txt | random_words.txt | 3 | 87.5 | 14 | 2 |
| train.txt | liberafolio_2020_09_09.txt | 2 | 98.54 | 405 | 6 |
| train.txt | liberafolio_2020_09_09.txt | 3 | 98.54 | 405 | 6 |
| train.txt | liberafolio_2020_09_16.txt | 2 | 95.67 | 309 | 14 |
| train.txt | liberafolio_2020_09_16.txt | 3 | 95.67 | 309 | 14 |
| train.txt | liberafolio_2020_09_22.txt | 2 | 98.05 | 251 | 5 |
| train.txt | liberafolio_2020_09_22.txt | 3 | 98.05 | 251 | 5 |

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
