from setuptools import setup, find_packages

setup(
    name='NotamMyWatch',
    version='0.1.0',
    url='https://github.com/Gabrieldowen/NOTAMyWatch',
    author='Gabriel Owen, Jacob Maslovskiy, Emily Ridge, Cole Essary, David Chavez, Brenden Dewitt',
    packages=find_packages(),    
    install_requires=[
        'flask',
        'airportsdata',
    ],
)