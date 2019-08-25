from setuptools import setup

setup(
    name='pymorpheus',
    version='0.1',
    description='Morpheus module for Python 3',
    author='Nick Celebic',
    author_email='nick@celebic.net',
    packages=['pymorpheus'],
    install_requires=[
        'requests',
        'urllib3',
        'json',
        'logging'
    ]
)
