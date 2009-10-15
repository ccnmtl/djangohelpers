from setuptools import setup, find_packages
import sys, os

version = '0.3dev'

long_description = open('README.txt').read()

setup(name='djangohelpers',
      version=version,
      description="a collection of useful middleware, template tags, etc",
      long_description=long_description,
      classifiers=[], 
      keywords='',
      author='Ethan Jucovy',
      author_email='ejucovy@gmail.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
      ],
      entry_points="""
      [console_scripts]
      maketemplatetag = djangohelpers.console_scripts:main
      """,
      )