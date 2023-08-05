# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='sval',  
    version='0.1.2',
    description='A fast Hold\'em seven card evaluator ',  
    long_description=long_description,  
    long_description_content_type='text/markdown',
    url='https://github.com/cstich/PySval',

    classifiers=[  
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='Texas Hold\'em, Hold\'em, Poker, 7 card, seven card',  # Optional
    packages=['sval'],
    python_requires='>=3.6',
    install_requires=['numba', 'numpy'], 
    include_package_data=True,

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={  
        'sval': ['lookup7card.dat.gz'],
    }
)
