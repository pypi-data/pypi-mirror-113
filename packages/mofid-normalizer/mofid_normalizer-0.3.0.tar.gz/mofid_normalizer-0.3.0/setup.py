from setuptools import find_packages, setup
setup(
    name='mofid_normalizer',
    packages=find_packages(include=['mofid_normalizer']),
    version='0.3.0',
    install_requires=["nltk","num2fawords","spacy","googledrivedownloader"],
    description='first version of Mofid Normalizer',
    author='ali96ebrahimi@gmail.com',
    license='MIT',
    include_package_data=True
)