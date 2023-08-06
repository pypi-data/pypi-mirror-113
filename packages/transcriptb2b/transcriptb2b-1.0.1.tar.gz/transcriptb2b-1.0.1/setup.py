import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="transcriptb2b",
    version="1.0.1",
    author="Bio2Byte",
    author_email="jose.gavalda.garcia@vub.be",
    description="A small example package for transcripting DNA to RNA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/agdiaz/bioinformatics-102",
    project_urls={
        "Bug Tracker": "https://bitbucket.org/agdiaz/bioinformatics-102/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)