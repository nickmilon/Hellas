'''
Created on Feb 24, 2013
@author: nickmilon
see: https://docs.python.org/2/distutils/setupscript.html
'''
from setuptools import setup, find_packages

version = '0.1.0'


print('installing packages:{!s}'.format(find_packages()))

setup(
    packages=find_packages(),
    name="Hellas",
    version=version,
    author="nickmilon",
    author_email="nickmilon/gmail/com",
    maintainer="nickmilon",
    url="https://github.com/nickmilon/Hellas",
    description="python utilities",
    long_description="see: readme",
    download_url="https://github.com/nickmilon/Hellas",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: HTTP"
        ],
    license="GPL3",
    keywords=["python", "utilities"],
    zip_safe=False,
    tests_require=["nose"],
    install_requires=[],
)
