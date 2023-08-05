import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="nerdpool-client",
    version="v1.0.0",
    author="Peter Andorfer",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email="peter.andorfer@oeaw.ac.at",
    description="A client for Nerdpool-Api",
    url="https://github.com/acdh-oeaw/nerdpool-client",
    license='MIT',
    packages=['nerdpool_client'],
    zip_safe=False,
    install_requires=[
        'requests',
    ],
)
