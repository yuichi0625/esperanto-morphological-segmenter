from glob import glob
from setuptools import find_packages, setup

setup(
    name='e_segmenter',
    version='0.1.0',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[],
    data_files=[
        ('e_segmenter', ['src/word_segmenter.py']),
        ('data', ['EsperantoWordSegmenter/experiments/train.txt']),
        ('data/sets', glob('EsperantoWordSegmenter/morphemesByType/sets/*.txt'))
    ]
)
