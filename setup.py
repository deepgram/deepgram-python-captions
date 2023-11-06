from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

VERSION = "0.0.2"
DESCRIPTION = "A Python package for generating captions."

setup(
    name="deepgram-captions",
    version=VERSION,
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
