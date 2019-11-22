from setuptools import setup, find_packages

setup(
    name='pysrc',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pytest',
    ]
)
