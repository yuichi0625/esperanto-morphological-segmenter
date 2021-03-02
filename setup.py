from pathlib import Path
from setuptools import find_packages, setup

training_file = Path('EsperantoWordSegmenter/experiments/train.txt')
morphemes_by_type_directory = Path('EsperantoWordSegmenter/morphemesByType/sets')

setup(
    name='esperanto_word_segmenter',
    version='0.1.0',
    packages=find_packages(),
    py_modules=['esperanto_word_segmenter'],
    python_requires='>=3.6',
    install_requires=[],
    data_files=[
        (str(training_file.parent), [str(training_file)]),
        (str(morphemes_by_type_directory), [str(p) for p in morphemes_by_type_directory.glob('*.txt')])
    ]
)
