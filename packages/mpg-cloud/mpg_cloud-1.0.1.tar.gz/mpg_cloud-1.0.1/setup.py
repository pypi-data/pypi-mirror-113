import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="mpg_cloud",
    version="1.0.1",
    description="Manage files in MPG Cloudservices.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.gwdg.de/hbenne/mpg_cloud.git",
    author="Hannes Benne",
    author_email="hbenne@mpiwg-berlin.mpg.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=[""],
    include_package_data=True,
    py_modules = ["mpg_cloud","seafile"],
    install_requires = ["lxml", "beautifulsoup4", "requests"],
    package_dir={'':'src'},
)

