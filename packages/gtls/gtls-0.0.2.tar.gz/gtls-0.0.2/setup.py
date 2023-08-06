import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gtls", 
    version="0.0.2",
    author="FutureNear",
    author_email="futurenear@163.com",
    description="Some simple tools commonly used in work.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FutureNear/Gtls.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
