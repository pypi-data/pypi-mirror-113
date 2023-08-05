
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ykbbb",
    version="1.0.0",
    author="yunkai.wang",
    author_email="wangyunkai0901@163.com",
    description="More convenient to process biological data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    #project_urls={
    #    "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    #},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
