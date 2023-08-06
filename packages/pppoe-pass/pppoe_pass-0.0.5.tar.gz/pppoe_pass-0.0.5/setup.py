from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


def check_dependencies():
    install_requires = []

    # Make sure dependencies exist

    try:
        import ipaddress
    except ImportError:
        install_requires.append('ipaddress')
    try:
        import socket
    except ImportError:
        install_requires.append('socket')
    try:
        import json
    except ImportError:
        install_requires.append('json')
    try:
        import requests
    except ImportError:
        install_requires.append('requests')
    try:
        import beautifulsoup4
    except ImportError:
        install_requires.append("beautifulsoup4")
    try:
        import re
    except ImportError:
        install_requires.append('re')

    return install_requires


if __name__ == "__main__":
    install_requires = check_dependencies()
setup(
    name='pppoe_pass',
    version='0.0.5',
    description='Router_pppoe',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Nair',
    author_email='',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=install_requires,

)

