from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='konval',
      version=version,
      description="A framework for data validation & conversion",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='validation conversion',
      author='Paul-Michael Agapow',
      author_email='pma@agapow.net',
      url='http://www.agapow.net',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
