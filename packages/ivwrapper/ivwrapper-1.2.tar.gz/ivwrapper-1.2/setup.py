from setuptools import find_packages, setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ivwrapper",
    version="1.2",
    description="Asynchroniczny wrapper dla api ivall'a.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nohet/ivwrapper",
    author="Nohet",
    author_email="igorczupryniak503@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="api, ivall api wrapper, wrapper",
    packages=find_packages(),
    install_requires=["aiohttp"],
)
