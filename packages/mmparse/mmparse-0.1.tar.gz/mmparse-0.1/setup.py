from distutils.core import setup

setup(
    name='mmparse',
    version='0.1',
    description='Parse Matrix Market Files',
    author='Michel Pelletier',
    author_email='michel@graphegon.com',
    url='https://github.com/michelp/mmparse',
    packages=['mm'],
    tests_require=["pytest"],
)
