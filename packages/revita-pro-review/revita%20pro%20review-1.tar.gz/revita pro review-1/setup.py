import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
      # pip3 revita pro review
    name="revita pro review", # Replace with your own username
    version="1",
    author="revita pro review",
    author_email="admin0@revita.com",
    description="revita pro review",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://88296arqzup28kbnqfnqk9tkuk.hop.clickbank.net/?tid=PYPI",
    project_urls={
        "Bug Tracker": "https://github.com/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
