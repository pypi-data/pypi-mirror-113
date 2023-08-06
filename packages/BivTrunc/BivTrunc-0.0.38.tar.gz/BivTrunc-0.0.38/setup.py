import setuptools

from numpy.distutils.core import Extension, setup

Libs = [Extension(name='BivTrunc.BivTruncF', sources=['BivTruncF.f90'], libraries=['lapack'])]

setup(
    name='BivTrunc',
    version='0.0.38',
    ext_modules = Libs,
    packages=setuptools.find_packages(exclude=['tests*']),
    license='MIT',
    description='Bivariate density estimation under irregular truncation',
    long_description=open('README.txt').read(),
    install_requires=['numpy', 'scipy'],
    author='Chad Schafer',
    author_email='cschafer@cmu.edu'
)
