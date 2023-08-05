#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()


test_requirements = [ ]

setup(
    author="Ana Sofia Carmo",
    author_email='anascacais@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="EpiBOX is a Raspberry Pi tool for easy signal acquisition.",
    entry_points={
        'console_scripts': [
            'epibox=epibox.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description_content_type='text/markdown',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['epibox', 'signal acquisition', 'Raspberry Pi'],
    name='epibox',
    packages=find_packages(include=['epibox', 'epibox.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/anascacais/epibox',
    download_url ='https://github.com/anascacais/epibox/archive/refs/tags/v0.1.0.tar.gz',
    version='0.1.0',
    zip_safe=False,
)
