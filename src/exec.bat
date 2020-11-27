@echo off

echo Create "result" directory to save result files
mkdir result

echo -----------------
set input=..\EsperantoWordSegmenter\experiments\test.txt
set output=result\test_result.txt
echo Execute for %input%
python word_segmenter.py %input% -o %output% -b
python calc_accuracy.py -a %input% -p %output%

echo -----------------
set input=..\eval_data\random_words.txt
set output=result\random_words_result.txt
echo Execute for %input%
python word_segmenter.py %input% -o %output% -b
python calc_accuracy.py -a %input% -p %output% -s

echo -----------------
set input=..\eval_data\liberafolio_2020_09_09.txt
set output=result\liberafolio_2020_09_09_result.txt
echo Execute for %input%
python word_segmenter.py %input% -o %output% -b
python calc_accuracy.py -a %input% -p %output% -s

echo -----------------
set input=..\eval_data\liberafolio_2020_09_16.txt
set output=result\liberafolio_2020_09_16_result.txt
echo Execute for %input%
python word_segmenter.py %input% -o %output% -b
python calc_accuracy.py -a %input% -p %output% -s

echo -----------------
set input=..\eval_data\liberafolio_2020_09_22.txt
set output=result\liberafolio_2020_09_22_result.txt
echo Execute for %input%
python word_segmenter.py %input% -o %output% -b
python calc_accuracy.py -a %input% -p %output% -s