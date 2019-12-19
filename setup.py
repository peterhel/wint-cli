from setuptools import setup

setup(name='wint-cli',
    version='0.1',
    description='Command line interface for Wint',
    url='https://github.com/peterhel/wint-cli',
    author='Peter Helenefors',
    author_email='peter@constructions.se',
    license='MIT',
#     packages=['wint-cli'],
    install_requires=['colorclass', 'terminaltables', 'requests', 'pygments'],
    zip_safe=False)