import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
    # pip3 wood profits review , wood profits amazon
    name="wood profits review", # Replace with your own username
    version="1",
    author="wood profits review",
    author_email="admin@code.com",
    description="wood profits review",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://8ab5bcio-tl3enfltegowbv8-f.hop.clickbank.net/?tid=PYPI",
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
