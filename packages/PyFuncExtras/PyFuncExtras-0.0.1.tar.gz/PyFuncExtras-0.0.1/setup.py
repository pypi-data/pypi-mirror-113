import setuptools

long_description = open("README.md", "r", encoding="utf-8").read()

setuptools.setup(
    name="PyFuncExtras",
    version="0.0.1",
    author="EnderBender",
    author_email="arjunrules55@gmail.com",
    description="extra python functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EnderBender08/pyfextras",
    project_urls={
        "Bug Tracker": "https://github.com/EnderBender08/pyfextras/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
