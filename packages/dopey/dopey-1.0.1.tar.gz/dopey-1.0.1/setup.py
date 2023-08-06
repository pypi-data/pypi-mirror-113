import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="dopey",
    version="1.0.1",
    description="A brainfuck interpreter made using python.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/gio101046/dopey",
    author="Giovani Rodriguez",
    author_email="me@grodriguez.dev",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["dopey"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dopey=dopey.dopey:_main",
        ]
    },
)