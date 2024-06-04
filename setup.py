from setuptools import setup, find_packages

version = '0.25'

long_description = open('README.txt').read()

setup(name='djangohelpers',
      version=version,
      description="a collection of useful middleware, template tags, etc",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author='Ethan Jucovy',
      author_email='ctl-dev@columbia.edu',
      url='https://github.com/ccnmtl/djangohelpers',
      license='BSD',
      packages=find_packages(include=['djangohelpers', 'djangohelpers.*']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'django',
          'six',
      ],
      entry_points="""
      [console_scripts]
      maketemplatetag = djangohelpers.console_scripts:main
      """,
      )
