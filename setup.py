from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="OPENING-RECOMMENDER",
    version="0.1",
    author="Rohan Manvatkar",
    packages=find_packages(),
    install_requires = requirements,
)