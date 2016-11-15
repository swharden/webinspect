from distutils.core import setup

import webinspect

setup(
    name='webinspect',
    version=webinspect.__version__,
    author='Scott W Harden',
    author_email='SWHarden@gmail.com',
    packages=['webinspect'],
    url='http://www.SWHarden.com',
    license='MIT License',
    description='Inspect python objects in a web browser.',
    long_description=open('README.md').read(),
)