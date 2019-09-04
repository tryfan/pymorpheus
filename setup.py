import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pymorpheus',
    version='0.1.5',
    description='Morpheus API wrapper for Python 3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nick Celebic',
    author_email='nick@celebic.net',
    license='MIT License',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'requests',
        'urllib3'
    ]
)
