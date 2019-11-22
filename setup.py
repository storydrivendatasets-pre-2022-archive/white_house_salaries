from setuptools import setup, find_packages

setup(
    name='whsa',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'openpyxl',
        'requests',

    ]
)
