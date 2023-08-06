import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oneflow-utils",
    version="0.0.1",
    author="Ren Tianhe",
    author_email="596106517@qq.com",
    description="deeplearning utils based on OneFlow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rentainhe/oneflow-utils.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)