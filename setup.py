from setuptools import setup
from pyutils import __version__

setup(
    name='pyutils',
    version=__version__,
    author='Anke Tang',
    description='my python toolkit',
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'tqdm',
        'classopt'
    ],
    scripts=[
        'scripts/pyutils_print_json.py',
        'scripts/pyutils_print_h5.py'
    ]
)
