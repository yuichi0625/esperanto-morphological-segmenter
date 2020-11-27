#!/bin/sh

echo Create "result" directory to save result files
mkdir -p result

echo -----------------
input="../EsperantoWordSegmenter/experiments/test.txt"
output="result/test_result.txt"
echo Execute for $input
python3 word_segmenter.py $input -o $output -b
python3 calc_accuracy.py -a $input -p $output

echo -----------------
input="../eval_data/random_words.txt"
output="result/random_words_result.txt"
echo Execute for $input
python3 word_segmenter.py $input -o $output -b
python3 calc_accuracy.py -a $input -p $output -s

echo -----------------
input="../eval_data/liberafolio_2020_09_09.txt"
output="result/liberafolio_2020_09_09_result.txt"
echo Execute for $input
python3 word_segmenter.py $input -o $output -b
python3 calc_accuracy.py -a $input -p $output -s

echo -----------------
input="../eval_data/liberafolio_2020_09_16.txt"
output="result/liberafolio_2020_09_16_result.txt"
echo Execute for $input
python3 word_segmenter.py $input -o $output -b
python3 calc_accuracy.py -a $input -p $output -s

echo -----------------
input="../eval_data/liberafolio_2020_09_22.txt"
output="result/liberafolio_2020_09_22_result.txt"
echo Execute for $input
python3 word_segmenter.py $input -o $output -b
python3 calc_accuracy.py -a $input -p $output -s