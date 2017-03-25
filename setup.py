#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from setuptools import setup

setup(

	name				='googlespreadsheet2django',
	version 			='1.0.0',
	description 		="""""",
	author  			='Ricardo Ribeiro',
	author_email		='ricardojvr@gmail.com',
	license 			='MIT',

	
	packages=[
		'googlespreadsheet2django',
		'googlespreadsheet2django.answers',
		'googlespreadsheet2django.models'
		],

	install_requires=['xlrd', 'requests', 'argparse'],

	entry_points={
		'console_scripts':['gsheet2django=googlespreadsheet2django.builder:main']
	}
)