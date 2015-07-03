#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    print("setuptools is missing. Install it using your package "
        + "manager (usually python-setuptools) or via pip (pip"
        + " install setuptools).")

setup(name= "blakey",
    version = "0.1.0",
    description = "Programmable drum machine",
    long_description = """Programmable drum machine""",
    author = "Bart Spaans",
    author_email = "bart.spaans@gmail.com",
    url = "https://github.com/bspaans/mingus-blakey",
    packages = ['blakey'],
    license="GPLv3",
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Artistic Software',
        'Topic :: Education',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: MIDI',
        ],
    entry_points = { 
        'console_scripts': [
            'blakey = blakey.blakey:main'
        ]
    }
)
