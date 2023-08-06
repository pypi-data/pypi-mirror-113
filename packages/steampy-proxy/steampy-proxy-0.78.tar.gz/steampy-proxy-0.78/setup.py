from setuptools import setup
import sys

if not sys.version_info[0] == 3 and sys.version_info[1] < 5:
    sys.exit('Python < 3.5 is not supported')

version = '0.78'

setup(
    name='steampy-proxy',
    packages=['steampy', 'test', 'examples', ],
    version=version,
    description='A Steam lib for trade automation',
    author='Michał Bukowski',
    author_email='gigibukson@gmail.com',
    license='MIT',
    url='https://github.com/hairygeek/steampy',
    keywords=['steam', 'trade', ],
    classifiers=[],
    install_requires=[
        "requests",
        "beautifulsoup4",
        "rsa",
        'tenacity'
    ],
)
