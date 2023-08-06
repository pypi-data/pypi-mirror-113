import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codec-Watteco",
    version="0.0.8",
    author="Olivier",
    author_email="ostephan@nke.fr",
    description="This codec is used to encode the data to send to the nke Watteco sensor. And to decode the received data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Watteco/Codec-Report-Standard-Python",
    project_urls={
        "Bug Tracker": "https://github.com/Watteco/Codec-Report-Standard-Python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
            "construct == 2.8.12",
            "dicttoxml"
      ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)