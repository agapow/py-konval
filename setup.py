from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='konval',
	version=version,
	description="Routines for data validation & conversion",
	long_description=open("README.txt").read() + "\n" +
		open(os.path.join("docs", "HISTORY.txt")).read(),
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Natural Language :: English',
		'Topic :: Text Processing :: General',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Operating System :: OS Independent',
		'Topic :: Text Processing :: Filters',
	], 
	keywords='validation conversion',
	author='Paul-Michael Agapow',
	author_email='pma@agapow.net',
	url='http://www.agapow.net/software/py-konval',
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
	test_suite='nose.collector',
)
