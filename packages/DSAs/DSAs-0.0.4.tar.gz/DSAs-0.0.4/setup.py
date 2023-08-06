from os import path
from setuptools import setup, find_packages

version = "0.0.4"

directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='DSAs',
    version=version,
    author='discretegames',
    author_email='discretizedgames@gmail.com',
    description="Python 3 implementations of various data structures & algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/discretegames/DSAs',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license="MIT",
    keywords=['python', 'data structure', 'algorithm', 'dsa'],
    project_urls={"GitHub": "https://github.com/discretegames/DSAs",
                  "PyPI": "https://pypi.org/project/DSAs"},
    python_requires='>=3',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ]
)
