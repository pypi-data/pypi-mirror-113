from setuptools import setup

setup(
    name='mallows_models',
    version='0.1.0',    
    description='A python package to for Mallows Model with top-$k$ and complete rankings using both Kendall\'s tau and Hamming distances.',
    url='https://github.com/ekhiru/top-k-mallows',
    author='Ahmed Boujaada and Ekhine Irurozki',
    author_email='aboujaada@bcamath.org',
    license='',
    keywords=['Mallows models', 'Top-k rankings', 'Permutations', 'Kendall\'s tau distance', 'Hamming distance', 'Rankings', 'Complete rankings'],
    packages=['mallows_models'],
    install_requires=['numpy',
    'scipy'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
