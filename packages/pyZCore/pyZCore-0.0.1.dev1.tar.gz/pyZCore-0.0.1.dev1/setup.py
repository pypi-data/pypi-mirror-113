import setuptools
from setuptools import version

with open("README.md", 'r') as ld:
    long_description = ld.read()

setuptools.setup(
    name="pyZCore",
    version="0.0.1.dev1",
    author="Aduri Sri Sambasiva Advaith",
    author_email="advaith.aduri@gmail.com",
    description="IP manager for ZCore Repository",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        'source':'https://github.com/advaith-aduri/pyZCore/'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)