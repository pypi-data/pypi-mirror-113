"""cloudfn meta-package config"""

from setuptools import setup
from setuptools import find_namespace_packages

PACKAGE_VERSION = '0.1'

setup(
	name='cloudfn',
	version=PACKAGE_VERSION,
	description='cloudfn',
	url='https://github.com/akrymskiy/cloudfn',
	author='Aleksandr Krymskiy',
	author_email='alex@krymskiy.net',
	license='MIT',
	packages=find_namespace_packages(include=['cloudfn', 'cloudfn.*']),
	install_requires=[
		f'cloudfn-core=={PACKAGE_VERSION}',
		f'cloudfn-aws=={PACKAGE_VERSION}'
	],
	entry_points = {
		'console_scripts': ['cfn=cfn.core.cli:main'],
	},
	zip_safe=False,
	python_requires=">=3.6.2"
)
