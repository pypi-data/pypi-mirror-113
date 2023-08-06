import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "decode_from_scratch",
    version = "1.1",
    author = "aidaner",
    author_email = "should@i.add",
    description = ("you can use this for scratch."),
    license = "BSD",
    keywords = "scratch server",
    url = "https://github.com/aidaner/decode_from_scratch",
    packages=['decode_from_scratch'],
    long_description= ('to use in projects'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
