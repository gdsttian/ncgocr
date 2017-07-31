#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

version = '0.2.0'

with open('requirements.txt') as f:
    requirements = f.read().split('\n')

test_requirements = [
    # TODO: put package test requirements here
]

input_fns = ['input/'+fn for fn in '11532192.txt 11597317.txt 11897010.txt 12079497.txt 12546709.txt 12585968.txt'.split(' ')]
setup(
    name='mcgocr',
    version=version,
    description="Micro Concept Gene Ontology Concept Recognition",
    long_description=readme,
    author="Chia-Jung, Yang",
    author_email='jeroyang@gmail.com',
    url='https://github.com/jeroyang/mcgocr',
    packages=[
        'mcgocr',
        'experiment'
    ],
    package_dir={'mcgocr': 'mcgocr',
                 'experiment': 'experiment'},
    data_files=[('input', input_fns)],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='mcgocr',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
