import setuptools
import os

datafiles = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk('pm/data')]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="power-music",
    version="0.0.0.1",
    author="DartBird",
    author_email="jintechdevel@gmail.com",
    description="Convert music site charts to youtube links",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dart-bird/power-music",
    packages=setuptools.find_packages(),
    install_requires=["beautifulsoup4","requests","unlimited-youtube-search"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)