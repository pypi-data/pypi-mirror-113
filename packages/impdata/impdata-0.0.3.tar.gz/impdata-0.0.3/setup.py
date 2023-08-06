import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="impdata", 
    version="0.0.3",
    author="FutureNear",
    author_email="futurenear@163.com",
    description="A tool for load  data into postgresql/mysql",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FutureNear/impdata.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "gtls>=0.0.1",
    ],
)
