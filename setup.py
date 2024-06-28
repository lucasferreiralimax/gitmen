from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gitman",
    version="0.1.4",
    description="CLI tool for managing GitHub projects, updating dependencies, and checking project statuses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucasferreiralimax/gitman",
    author="lucasferreiralimax",
    author_email="lucasferreiralimax@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
    ],
    python_requires=">=3.12",
    py_modules=["gitman.main"],
    entry_points={
        "console_scripts": [
            "gitman = gitman.main:app",
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "gitman": ["translations/*.yml"],
    },
    install_requires=["python-i18n", "inquirer"],
    keywords="github cli projects dependencies",
)
