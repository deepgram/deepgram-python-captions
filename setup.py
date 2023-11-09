from setuptools import setup, find_packages
import os.path

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

with open(
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "deepgram_captions", "_version.py"
    ),
    encoding="utf8",
) as file:
    exec(file.read())
# imports as __version__

DESCRIPTION = "A Python package for generating captions."

setup(
    name="deepgram-captions",
    version=__version__,
    author="Deepgram",
    author_email="devrel@deepgram.com",
    url="https://github.com/deepgram/deepgram-python-captions",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "dev": [
            "black",
            "pytest",
        ],
    },
    keywords=["deepgram", "captions", "srt", "webvtt"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Text Processing :: General",
    ],
)
