from setuptools import find_packages, setup

setup(
    name='recipe-tagger',
    packages=find_packages(include=['recipe_tagger']),
    version='0.2.0',
    description='A library for tagging and classify recipes',
    author='Andrea Turconi',
    license='MIT',
    url='https://github.com/TurconiAndrea/recipe-tagger',
    download_url='https://github.com/TurconiAndrea/recipe-tagger/archive/refs/tags/0.2.0.tar.gz',
    keywords=['food', 'recipe', 'tag', 'tagging', 'ingredient'],
    install_requires=['wikipedia', 'PyDictionary', 'textblob', 'pyfood', 'unidecode'],
    test_suite='tests',
    include_package_data=True,
    package_data={'': ['data/*.npy']},
)