from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy

extensions = cythonize([Extension("gravitylab.solvers", ["gravitylab/solvers.pyx"])])
cmdclass = {"build_ext" : build_ext}

setup(
    name="GravityLab",
    version="2.2.6",
    packages=find_packages(),
    license="MIT",
    author="Kushaal Kumar Pothula",
    author_email="kushaalkumar.astronomer@gmail.com",
    url = "https://github.com/Kushaalkumar-pothula/gravitylab",
    description="A fast astrophysical N-body simulator",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    cmdclass=cmdclass,
    ext_modules=extensions,
    include_dirs=[numpy.get_include()],
    install_requires = [
        'numpy>=1.20.0',
        'matplotlib>=3.3.2'
    ]
)