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
    long_description="""webinspect allows python developers to learn about objects' methods by displaying their properties in a web browser. This is extremely useful when trying to figure out how to use confusing and/or poorly documented classes. Just stick webinspect.launch(someObject) anywhere in your code and a web browser will automatically launch displaying all of the information about the object. See examples on the documentation page.""",
)