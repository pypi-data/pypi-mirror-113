from setuptools import setup, find_packages
 
classifiers = []
 
setup(
	name='pypiapijson',
	version='1.9.7',
	description='A client for connect to pypi.org api to retrieve the python packages!',
	long_description=open('README.md').read() + "\n# Read the doc in github that we provided link too!\n# Also new version is more good thing too!",
	long_description_content_type='text/markdown',
	url='https://github.com/I-make-python-module-and-bots-stuff/pypiapijson',  
	author='Rukchad Wongprayoon',
	author_email='mooping3roblox@gmail.com',
	license='MIT', 
	classifiers=classifiers,
	keywords='Tools', 
	packages=find_packages(),
	install_requires=[]
)
