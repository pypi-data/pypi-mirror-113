"""Build and install pupygrib."""

from setuptools import find_packages, setup  # type: ignore [import]

with open("README.md", encoding="utf-8") as stream:
    long_description = stream.read()

setup(
    name="pupygrib",
    version="0.8.0",
    description="A light-weight pure Python GRIB reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gorilladev/pupygrib",
    author="Mattias Jakobsson",
    author_email="mattias.jakobsson@smhi.se",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Typing :: Typed",
    ],
    keywords="grib grid data meteorology",
    packages=find_packages("src"),
    package_data={"pupygrib": ["py.typed"]},
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "importlib-metadata >= 1.0 ; python_version < '3.8'",
        "numpy",
    ],
)
