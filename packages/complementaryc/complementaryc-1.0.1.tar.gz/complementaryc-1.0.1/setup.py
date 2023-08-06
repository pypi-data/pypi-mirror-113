import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="complementaryc",
    version="1.0.1",
    author="Bio2Byte",
    author_email="jose.gavalda.garcia@vub.be",
    description="AA small example package for complementary DNA conversion and telling the year",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/agdiaz/bioinformatics-101",
    project_urls={
        "Bug Tracker": "https://bitbucket.org/agdiaz/bioinformatics-101/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
    package_data={"complementaryc": ["bin/*"]}
)
