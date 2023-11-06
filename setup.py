from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A Python package for generating captions."
LONG_DESCRIPTION = """
This package provides utilities to transform speech-to-text API responses into SRT or WebVTT captions.
It is designed to simplify the process of converting audio transcriptions into readable caption formats.
"""

setup(
    name="deepgram-captions",
    version=VERSION,
    author="Deepgram",
    author_email="devrel@deepgram.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/plain",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "dev": [
            "black",
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
