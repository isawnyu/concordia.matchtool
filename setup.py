from setuptools import setup, find_packages
import os

version = '0.1'
readme = open('README.txt', 'rb').read()

setup(name='concordia.matchtool',
      version=version,
      description="'Attempt rule-based matching of content across two data files'",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author="'Tom Elliott'",
      author_email="'tom.elliott@nyu.edu'",
      url="'http://concordia.atlantides.org'",
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['concordia'],
      include_package_data=True,
      zip_safe=True,
      test_suite='concordia.matchtool.tests.test_suite',      
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
