# setup.py
from setuptools import setup

README = open("README.md", "r").read()
print(README)
setup(
    name="fig_dash",
    version="0.0.1",
    packages=["fig_dash"],
    package_dir={"": 'fig_dash'},
    url="https://github.com/atharva-naik/fig-dash",
    license="GPLv3+",
    long_description=README,
    author="Atharva Naik",
    author_email="atharvanaik2018@gmail.com",
    description="Browser and Dashboard to boost poductivity",
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Browser',
        'Topic :: Dashboard',
    ],
)