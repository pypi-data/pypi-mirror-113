import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="trolldb",
    version="1.2.1",
    description="JSON Database but just encrypted",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ProYT303/trollDB",
    author="Walterepic",
    author_email="social.proyt303@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["trolldb", "cryptography"],
    include_package_data=True,
    install_requires=["cryptography"],
    entry_points={
        "console_scripts": [
        ]
    },
)