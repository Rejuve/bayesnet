import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bayes", # Replace with your own username
    version="0.0.1",
    author="Deborah Duong",
    author_email="deborah@singularitynet.io",
    description="protobuf based bayesian network service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rejuve/covid-bayesnet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
