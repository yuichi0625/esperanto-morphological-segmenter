This is a reimplementation of [EsperantoWordSegmenter](https://github.com/tguinard/EsperantoWordSegmenter) in Python, which is a tool for segmenting Esperanto words into morphemes.

This Python implementation has some modifications from the original one (for instance, training markov model is seperated from segmenting words).

The original paper is [here](https://ufal.mff.cuni.cz/pbml/105/art-guinard.pdf).

## Installation
```
git clone 
```

**Requirements**
- Python >= 3.

## Usage

## Accuracy
| train data | eval data | n_gram | accuracy (%) | correct (pcs) | incorrect (pcs) |
| --- | --- | --- | --- | --- | --- |
| train.txt | test.txt | 2 | 97.51 | 10328 | 263 |
| train.txt | test.txt | 3 | 97.49 | 10326 | 265 |
| train.txt<br>test.txt | test.txt | 2 | 97.54 | 10331 | 260 |
| train.txt<br>test.txt | test.txt | 3 | 97.57 | 10334 | 257 |
| train.txt | liberafolio_2020_09_22.txt | 2 | 97.65 | 625 | 15 |
| train.txt | liberafolio_2020_09_22.txt | 3 | 97.81 | 626 | 14 |
| train.txt | random_words.txt | 2 | 81.25 | 13 | 3 |
| train.txt | random_words.txt | 3 | 87.5 | 14 | 2 |

## Problems to be solved
There are some problems in the original repository.

### Morphemes by Types
1. morphemesByType contains some confusing words, which interrupt prediction, e.g.
    1. "konat" (-> "kon" + "at")
    1. "egoism" (-> "ego" + "ism")
    1. "solist" (-> "sol" + "ist")

### Dataset
1. The annotated train and test files include lots of falsely annotated words, e.g.
    - `Incorrect segmentation`:
        1. teknologio as teknolog'i'o (-> teknologi'o)
        1. faceti as fac'et'i (-> facet'i)
        1. finio as fi'ni'o (-> fini'o)
        1. decentraligo as de'centr'al'ig'o (-> de'central'ig'o)
    - `Correct segmentation but incorrect tagging`:
        1. dis'kon'ig'o as adv'verb'noun'nounEnding (at least "ig" should be tagged as suffix)

### Markov Model
1. Some words are really difficult to segment, e.g.
    - `Both words exist`:
        1. farado as far'ad'o and farad'o
        1. esperanto as esper'ant'o and esperant'o
    - `Syntactically correct but semantically incorrect`:
        1. katokulo as kat'o'kul'o (-> kat'okul'o)
        1. ledpretigisto as led'pret'i'gist'o (-> led'pret'ig'ist'o)
        1. edziĝoringo as edz'iĝ'or'ing'o (-> edz'iĝ'o'ring'o)