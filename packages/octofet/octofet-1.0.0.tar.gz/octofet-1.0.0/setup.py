import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="octofet",
    version="1.0.0",
    description="Raspberry Pi library for working with the Amperka Octofet"
    " – 8-channels switch board.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/amperka/OctofetPi/",
    author="Amperka LLC",
    author_email="dev@amperka.com",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["octofet"],
    install_requires=["spidev"],
)
