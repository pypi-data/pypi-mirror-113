#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import exists, dirname, realpath
from setuptools import setup, find_packages
import sys



sys.path.insert(0, realpath(dirname(__file__))+"/"+'diffop')


setup(
    name='diffop',
    version='1.0.0',
    description='A Python package for finite difference derivatives in any number of dimensions.',
    long_description="""A Python package for finite difference derivatives in any number of dimensions.
    
    Features: 

        * Differentiate arrays of any number of dimensions along any axis
        * Partial derivatives of any desired order
        * Accuracy order can be specified
        * Accurate treatment of grid boundary
        * Includes standard operators from vector calculus like gradient, divergence and curl
        * Can handle uniform and non-uniform grids
        * Can handle arbitrary linear combinations of derivatives with constant and variable coefficients
        * Fully vectorized for speed
        * Calculate raw finite difference coefficients for any order and accuracy for uniform and non-uniform grids

    """,
    url='https://github.com/AdwardAllan',
    license='GNU License',
    author='Li XinJUN',
    author_email='lxjproductivity@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords=['finite-differences',  'numerical-derivatives', 'scientific-computing'],
    packages=find_packages(),
#     package_dir={'diffop': 'diffop'},
    include_package_data=True,
    install_requires=['numpy', 'scipy', 'sympy'],
    setup_requires=["pytest-runner"],
    python_requires=">=3.6",
    tests_require=["pytest"],
    platforms=['ALL'],
)
