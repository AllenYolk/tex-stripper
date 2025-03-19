from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="texstripper",
    version="0.1.0",
    author="AllenYolk (Yifan Huang, from Peking University)",
    author_email="allen.yfhuang@gmail.com",
    description="A tool to strip LaTeX files for Grammarly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AllenYolk/tex-stripper",
    packages=find_packages(),
    include_package_data=False,
    install_requires=[],
    entry_points={  # define the CLI
        "console_scripts": [
            "texstripper=texstripper.cli:main",  # command=module:function
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
