from setuptools import setup

setup(
	name='pysovryn',
	version='0.01',
	author='Jamiel Sheikh',
	packages=['pysovryn'],
	install_requires=[
		'matplotlib',
		'web3',
		'pandas',
		'datetime',
		'requests'
	],
	include_package_data=True,
)