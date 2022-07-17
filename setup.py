from setuptools import setup

setup(
    name='pyutils',
    version='0.1.0',
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
        'scripts/pyutils_print_json.py'
    ]
)
