from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = "0.0.2"
DESCRIPTION = "An infix-to-postfix expression parser for evaluating math expressions."

setup(
    name="tinypost",
    version=VERSION,
    author="Nathan Abraham",
    author_email="abnathan123@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=["python", "math", "shunting-yard",
              "parser", "expression evaluation"],
    classifiers=["Operating System :: Unix",
                 "Operating System :: MacOS :: MacOS X",
                 "Operating System :: Microsoft :: Windows",
                 ]
)
