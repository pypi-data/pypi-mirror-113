import setuptools

setuptools.setup(
    name="ccs_aws",
    version="2.1.0",
    author="code_duck",
    description="ccs aws modules",
    long_description_content_type="text/markdown",
    install_requires=['boto3'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)