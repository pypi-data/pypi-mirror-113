import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awsglue-questdb-writer",
    version="0.0.1",
    author="Dan Voyce",
    author_email="dan.voyce+pypi@tymlez.com",
    description="A simple writing utility for writing to QuestDB from PySpark / AWS Glue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tymlez/awsglue-questdb-writer",
    project_urls={
        "Bug Tracker": "https://github.com/Tymlez/awsglue-questdb-writer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)