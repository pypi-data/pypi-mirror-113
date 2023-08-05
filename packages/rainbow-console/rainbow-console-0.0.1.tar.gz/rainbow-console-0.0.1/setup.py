import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rainbow-console",
    version="0.0.1",
    author="Elysiumskrieger",
    author_email="kurt@i-e.space",
    description="This module is designed to color the information displayed in the console.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Elysiumskrieger/rainbow-console",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
