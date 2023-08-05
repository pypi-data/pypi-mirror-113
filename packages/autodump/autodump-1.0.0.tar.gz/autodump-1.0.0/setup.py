import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autodump",
    version="1.0.0",
    author="Ping Z.",
    author_email="ping69852@gmail.com",
    description="Automatically and non-invasively dump your (experiment) data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noilreed/autodump",
    project_urls={
        "Bug Tracker": "https://github.com/noilreed/autodump/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["test"]),
    install_requires=['mysql-connector-python >= 8.0.25', 'PyYAML'],
    python_requires=">=3.6",
)
