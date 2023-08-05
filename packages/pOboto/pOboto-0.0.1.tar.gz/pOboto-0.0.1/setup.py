
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pOboto",
    version="0.0.1",
    author="jujbates",
    author_email="justin.bates@productops.com",
    description="It's pip... pO Boto Wrapper.",
    long_description=long_description,
    url="https://github.com/Justin-productOps/pO-boto",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)