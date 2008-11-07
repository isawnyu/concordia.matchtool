Introduction
============

We need a real readme, but for now.

a framework for defining and executing match rulesets for relating content in two datasets with different schemata

original use case is getting matches between print-style BAtlas citations held in aphrodisias inscriptions xml and our batlas ids

concordia/matchtool/rules.py defines classes for building, managing and executing rulesets

concordia/matchtool/dset.py defines classes for managing datasets to be related (would/could build parsers to read data in various formats 
into this internal data structure, which rules.py then knows how to do stuff with)

concordia/matchtool/data.cfg provides configuration information (like relative or absolute paths to data files)

concordia/matchtool/tests/rule.txt contains some explanatory tests for the classes and methods in concordia/matchtool/rules.py

