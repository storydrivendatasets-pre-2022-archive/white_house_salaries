from setuptools import setup, find_packages

setup(
    name='whsal',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pytest',
        'openpyxl',
    ]
)
