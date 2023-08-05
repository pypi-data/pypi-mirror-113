from os import name
from setuptools import setup, find_packages
with open('README.rst', 'r', encoding='utf-8') as rd:
    long_description = rd.read()

setup(
    name='zqw_pkgs',
    version=1.4,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='quanwei.zheng',
    author_email='quanwei_275@126.com',
    maintainer='quanwei.zheng',
    maintainer_email='quanwei_275@126.com',
    license='BSD License',
    packages=find_packages(),
    platforms=['all'],
    url='',
    
)