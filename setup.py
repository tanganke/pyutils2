from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

__version__ = '0.1.0'

ext_modules = [
    Pybind11Extension(
        "pyutils.cppext",
        sorted(glob("src/*.cpp")),  # Sort source files for reproducibility
    ),
]

setup(
    name='pyutils',
    version=__version__,
    author='Anke Tang',
    description='my python toolkit',
    setup_requires=["pybind11"],
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
    ],
    packages=['pyutils'],
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules
)
