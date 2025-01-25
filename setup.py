from setuptools import setup

setup(
    name="dayplot",
    version="0.1.0",
    packages=["dayplot"],
    description="calendar heatmaps with matplotlib",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_data={"dayplot": ["data/*.csv"]},
    author="Joseph Barbier",
    author_email="joseph.barbierdarnal@gmail.com",
    url="https://github.com/JosephBARBIERDARNAL/dayplot",
    install_requires=["matplotlib"],
)
