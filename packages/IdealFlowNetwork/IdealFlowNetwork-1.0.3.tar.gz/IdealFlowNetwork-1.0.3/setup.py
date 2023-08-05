# -*- coding: utf-8 -*-
"""
@author: Kardi Teknomo
"""

# from distutils.core import setup
from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'IdealFlowNetwork',        
  packages = ['IdealFlowNetwork'], 
  package_dir={"": str("src")},  
  version = '1.0.3',
  platforms=['any'],
  license='GNU General Public License v3.0',   
  description = 'Ideal Flow Network Python Library',  
  author = 'Kardi Teknomo',                  
  author_email = 'teknomo@gmail.com',     
  url = 'http://people.revoledu.com/kardi/',   
  download_url = 'https://github.com/teknomo/IdealFlowNetwork/blob/Development/dist/IdealFlowNetwork-1.0.3.tar.gz',
  keywords = ['IFN', 'Markov', 'irreducible', 'premagic'],
  long_description=long_description,
  long_description_content_type='text/markdown',#"text/x-rst",
  install_requires=[           
          'numpy',
          'pandas',
      ],
  setup_requires=["wheel"],
  classifiers=[
    'Development Status :: 5 - Production/Stable',    
    'Intended Audience :: Developers', 
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Topic :: Education',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Software Development :: Libraries',
    'License :: Free for non-commercial use',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
    
  ],
)