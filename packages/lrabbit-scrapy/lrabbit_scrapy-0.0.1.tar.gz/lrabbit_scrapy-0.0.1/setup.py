import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lrabbit_scrapy",
    version="0.0.1",
    author="lrabbit",
    author_email="709343607@qq.com",
    description="this is a small decription",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/litter-rabbit/lrabbit_scrapy",
    project_urls={
        "Bug Tracker": "https://github.com/litter-rabbit/lrabbit_scrapy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "aiomysql>= 0.0.21",
        "aiohttp >= 3.7.3",
        "sqlalchemy ==1.4.0",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
