import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awspy",
    version="0.2.0",
    author="ScholarPack",
    author_email="dev@scholarpack.com",
    description="Utility tools for running Python services in AWS.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ScholarPack/awspy",
    packages=["aws_py", "aws_py.ecs"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["requests >= 2.26.0", "types-requests >= 2.25.0"],
)