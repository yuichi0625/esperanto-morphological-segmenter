# Reimplemented Esperanto Word Segmenter
This is a reimplementation of [EsperantoWordSegmenter](https://github.com/tguinard/EsperantoWordSegmenter) in Python (originally in Scala), which is a tool for segmenting Esperanto words into morphemes. The original paper is [here](https://ufal.mff.cuni.cz/pbml/105/art-guinard.pdf).

## Table of Contents
- [Requirements](#Requirements)
- [Installation](#Installation)
- [Usage](#Usage)
    - [src/word_segmenter.py](#srcword_segmenterpy)
    - [e_segmenter (as a package)](#e_segmenter-as-a-package)
- [Accuracy](#Accuracy)
- [Problems to be solved](#Problems-to-be-solved)

## Requirements
- Python >= 3.6

## Installation
```bash
$ git clone https://github.com/yuichi0625/reimplemented-esperanto-word-segmenter.git --recursive

# You don't need to install as a package if you just want to give it a try.
# Instead, please use src/word_segmenter.py
$ python setup.py install
```

## Usage
### src/word_segmenter.py
This is the reimplementation of [WordSegmenter.scala](https://github.com/tguinard/EsperantoWordSegmenter/blob/230cea85c7ed9a3e72962bf14385309cb41affd6/src/WordSegmenter.scala).

```bash
$ python src/word_segmenter.py input_file -b
```

`input_file` should contain one word for each row, for instance,
```bash
# examples.txt
animalo
belulino
certe
dependas
```


### e_segmenter (as a package)
```python
from e_segmenter import EsperantoWordSegmenter

segmenter = EspernatoWordSegmenter()
segmenter('belulino')  # -> "bel'ul'in'o"
segmenter('katojn')    # -> "kat'ojn" (word endings are concatenated)
segmenter('facebook')  # -> "" (if no valid segmentation is found)
```

CAUTION: If you try this in this directory (I mean `Path(README.md).parent`), it will raise an error because it will try to read e_segmenter in this directory directly, which is empty.

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
