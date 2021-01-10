import ast
from io import open
from setuptools import find_packages, setup

import os
with open('src/version.py', 'r') as f:
    for line in f:
        if line.startswith('VERSION'):
            version = ast.literal_eval(line.strip().split('=')[-1].strip())
            break

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()


os.system('pip install --user git+https://github.com/odwdinc/pyamiibo@master')


setup(
    name='ssbu_amiibo',
    version=version,
    description='SSBU Amiibo Editor',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Anthony Pray',
    author_email='anthony.pray@gmail.com',
    maintainer='Anthony Pray',
    maintainer_email='anthony.pray@gmail.com',
    url='https://github.com/odwdinc/SSBU_Amiibo',
    license='MIT',
    keywords=[
        '',
    ],

    install_requires=[
      'pyamiibo',
      'cryptography',
      'Pillow',
      'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=find_packages(),
    entry_points={
        'gui_scripts': [
            'pyhex = src.hex:maine',
            'ssbu_amiibo = src.ui:maine'
        ],
    },
)
