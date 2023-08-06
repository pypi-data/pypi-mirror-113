import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hhmmexperiments",
    version="1.0.0",
    author="Fernando",
    author_email="fmoreno@tsc.uc3m.es",
    description="First pip test",
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/fmorenopino/HeterogeneousHMM",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
)