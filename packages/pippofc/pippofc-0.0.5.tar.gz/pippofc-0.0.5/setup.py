from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: Microsoft :: Windows :: Windows 10',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3'	
]

setup(
	name='pippofc',
	version='0.0.5',
	description='An italian fiscal code calculator',
	long_description=open('README.md').read(),
	url='',
	author='ImVenomDev',
	author_email='imthetruevenom@gmail.com',
	license='MIT',
	classifiers=classifiers,
	keywords='fiscal code',
	packages=find_packages(),
	install_requires=['']
)	