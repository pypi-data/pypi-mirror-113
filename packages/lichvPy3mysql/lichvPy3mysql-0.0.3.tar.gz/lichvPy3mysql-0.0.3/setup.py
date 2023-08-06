from distutils.core import setup
from setuptools import find_packages

setup(
	name = 'lichvPy3mysql',
	version = '0.0.3',
	description = 'Utility tools with mysqldb',
	long_description = 'Utility tools with mysqldb', 
	author = 'lichv',
	author_email = 'lichvy@126.com',
	url = 'https://github.com/lichv/py3mysql',
	license = '',
	install_requires = [
		'pymysql>=1.0.2',
	],
	python_requires='>=3.6',
	keywords = '',
	packages = find_packages('src'),
	package_dir = {'':'src'},
	include_package_data = True,
)
