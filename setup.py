#!/usr/bin/env python3
from setuptools import find_packages, setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='Timecard-App',
    version='2.0.7',
    description='Track time beautifully.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jason C. McDonald',
    author_email='codemouse92@outlook.com',
    url='https://github.com/codemouse92/timecard',
    project_urls={
        'Bug Reports': 'https://github.com/codemouse92/timecard/issues',
        'Funding': 'https://github.com/sponsors/CodeMouse92',
        'Source': 'https://github.com/codemouse92/timecard',
    },
    keywords='time, tracking, office, clock, tool, utility',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    package_dir={'': 'src'},
    packages=find_packages(where='src'),

    include_package_data=True,

    python_requires='>=3.6, <4',
    install_requires=['PySide2 >= 5.15.0', 'appdirs >= 1.4.4'],

    extras_require={
        'test': ['pytest'],
    },

    entry_points={
        'gui_scripts': [
            'Timecard-App = timecard.__main__:main'
        ]
    }
)
