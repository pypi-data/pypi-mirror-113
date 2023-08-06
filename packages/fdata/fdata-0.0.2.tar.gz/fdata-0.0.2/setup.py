from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()
setup(
    name='fdata',
    version='0.0.2',
    description='FDA data and dataset creation tool',
    py_modules=['fdata_functions'],
    package_dir={'':'src'},

    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers = [
        "Programming Language :: Python :: 3", 
        "Programming Language :: Python :: 3.8", 
        "License :: OSI Approved :: MIT License", 
    ],

    install_requires = ['pandas >= 1.1'],

    extra_requires = {'dev': ['pytest' >= '6.1.1']},

    url = 'https://github.com/G-Sprouts/FDA_sae',
    author = 'Garrett Wankel',
    author_email = 'g.wankel.1@gmail.com'
)