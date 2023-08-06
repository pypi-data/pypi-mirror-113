from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='skuvault',
    packages=find_packages(include=['skuvault', 'skuvault.*']),
    version='1.1.0',
    description='A Python library for the SkuVault API',
    author='Nathan Head',
    author_email="headn90@gmail.com",
    license='MIT',
)
