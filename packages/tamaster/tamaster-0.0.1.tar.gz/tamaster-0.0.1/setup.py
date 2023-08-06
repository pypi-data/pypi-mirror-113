from setuptools import setup, find_packages
from tamaster import __version__

setup(
    name='tamaster',
    version=__version__,
    description='TA data interface implementation',
    author='puyuantech',
    author_email='info@puyuan.tech',
    packages=find_packages(),
    install_requires=[
        'requests >= 2.22.0',
    ]
)
