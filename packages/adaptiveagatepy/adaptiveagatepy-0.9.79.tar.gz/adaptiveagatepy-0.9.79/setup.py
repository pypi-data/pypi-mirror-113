import os
import setuptools

# read the contents of the README.md file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

buildNum = os.getenv("bamboo_buildNumber", default=1)

setuptools.setup(
    name="adaptiveagatepy",
    version="0.9." + str(buildNum),
    author="Adaptive Biotechnologies Corporation",
    author_email="agate-support@adaptivebiotech.com",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="http://www.adaptiveagate.com",
    description="Python APIs for accessing sequencing data in the Adaptive Biotechnologies Agate Datastore",
    packages=['adaptiveagatepy'],
    install_requires=[
        'requests',
        'pyodbc',
        'msal',
        'azure-storage-blob>=12.8',
        'pyarrow',
        'dask',
        'dask[dataframe]',
        'parameterized'
    ],
    package_dir={'': 'src'},
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
    ),
    data_files=[("", ["LICENSE.txt"])],
    test_suite='nose.collector',
    tests_require=['nose'],
)
