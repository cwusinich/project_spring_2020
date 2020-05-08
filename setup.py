from setuptools import setup, find_packages
 
with open('README.md','r') as yeet:
	long_description=yeet.read()

setup(
        name = 'MID_proc',
        author = 'Christina Wusinich',
        version = '0.2.0',
	author_email='christinawusinich@gmail.com',
        description = 'Some tools for processing MID behavioral and MEG data',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/cwusinich/project_spring_2020',
        license = 'Apache',
        packages = find_packages(),
	python_requires='>=3.6'
     )


