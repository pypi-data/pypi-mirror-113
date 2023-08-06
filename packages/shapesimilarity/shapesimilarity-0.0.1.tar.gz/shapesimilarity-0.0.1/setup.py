from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
  long_description = "\n" + fh.read()

setup(
  name='shapesimilarity',
  version='0.0.1',
  author='Nelson Wenner',
  packages=['shapesimilarity'],
  url='https://github.com/nelsonwenner/shape-similarity',
  description='Quantify the similarity between two shapes/curves',
  long_description_content_type="text/markdown",
  long_description=long_description,
  keywords=['python', 'curve', 'frechet-distance', 'procrustes-analysis'],
  platforms=['any']
)