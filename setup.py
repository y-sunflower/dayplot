from setuptools import setup

setup(
    name="dayplot",
    version="0.2.0",
    packages=["dayplot"],
    description="Calendar heatmaps with matplotlib",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    author="Joseph Barbier",
    author_email="joseph.barbierdarnal@gmail.com",
    url="https://github.com/JosephBARBIERDARNAL/dayplot",
    install_requires=["matplotlib"],
)
