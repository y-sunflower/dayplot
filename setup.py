from setuptools import setup

setup(
    name="dayplot",
    version="0.0.0.9",
    packages=["dayplot"],
    description="day plotting",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Joseph Barbier",
    author_email="joseph.barbierdarnal@gmail.com",
    url="https://github.com/JosephBARBIERDARNAL/dayplot",
    install_requires=["matplotlib"],
)
