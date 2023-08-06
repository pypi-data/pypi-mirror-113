__author__ = 'Brian M Anderson'
# Created on 07/20/2021


from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='DeleteFilesRapidly',
    author='Brian Mark Anderson',
    author_email='b5anderson@health.ucsd.edu',
    version='0.0.4',
    description='Tool for quickly deleting files on a remote server via threading',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'DeleteFilesRapidly': 'DeleteFilesRapidly'},
    packages=['DeleteFilesRapidly'],
    include_package_data=True,
    url='https://github.com/brianmanderson/Dicom_RT_and_Images_to_Mask',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
    install_requires=required,
)
