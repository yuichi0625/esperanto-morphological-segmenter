This is another reimplementation inspired by the original.

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
